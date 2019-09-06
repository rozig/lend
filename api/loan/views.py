import datetime
import math

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.loan.serializers import LoanDetailSerializer, PaymentDetailSerializer
from app.constants import MESSAGES
from app.core.paginations import StandardResultsSetPagination
from app.helpers import add_months, generate_transaction_id, is_eligible_lender
from app.models import Account, Loan, LoanProfile, LoanPayment, Transaction


class LoanView(generics.ListCreateAPIView):
    """
    API Endpoints for loan
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = LoanDetailSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Loan.objects.all()

    def post(self, request):
        user = request.user
        requested_amount = request.data.get('amount')
        requested_length = request.data.get('length')

        errors = {}

        if not requested_amount:
            errors['amount'] = [MESSAGES.get('FIELD_REQUIRED').format('This field')]

        if not requested_length:
            errors['length'] = [MESSAGES.get('FIELD_REQUIRED').format('This field')]

        loan_profile = LoanProfile.objects.filter(user=user)
        if loan_profile.exists():
            loan_profile = loan_profile.first()
            loans = self.get_queryset().prefetch_related('loanpayment_set').filter(user=user)

            for loan in loans:
                loan_finished = True
                total_amount = loan.amount + (loan.amount * loan.interest_rate / 100)
                amount = 0

                for payment in loan.loanpayment_set.filter(status='paid'):
                    amount += payment.amount
                if total_amount > amount:
                    loan_finished = False

                if not loan_finished:
                    return Response({
                        'detail': MESSAGES.get('UNPAID_LOAN')
                    }, status=status.HTTP_400_BAD_REQUEST)

            num_of_loans = len(loans)
        else:
            loan_profile = LoanProfile.objects.create(user=user, score=0)
            num_of_loans = 0

        lend_score = loan_profile.score

        eligibility = is_eligible_lender(
            requested_amount,
            requested_length,
            lend_score,
            num_of_loans)

        if not eligibility['eligible']:
            return Response({
                'detail': eligibility['reason']
            }, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.date.today()
        deadline = today.replace(year=today.year + math.ceil(requested_length / 12))
        loan_request = Loan.objects.create(
            user=user,
            amount=requested_amount,
            interest_rate=eligibility['interest_rate'],
            status='ongoing',
            deadline=deadline)

        account = Account.objects.get(user=user)
        account.balance += requested_amount
        account.updated_at = datetime.datetime.now()
        account.save()

        Transaction.objects.create(
            id=generate_transaction_id(),
            type='loan',
            amount=requested_amount,
            description='LOAN FOR {} {}'.format(user.first_name, user.last_name),
            account=account)

        payment_deadline = add_months(today, 1)

        payment_amount = requested_amount
        payment_amount += payment_amount * eligibility['interest_rate'] / 100
        payment_amount /= requested_length

        LoanPayment.objects.create(
            loan=loan_request,
            amount=payment_amount,
            status='pending',
            payment_date=None,
            deadline=payment_deadline)

        return Response({
            'id': loan_request.id,
            'monthly_payment_amount': payment_amount,
            'loan_length': requested_length,
            'loan_amount': requested_amount,
            'interest_rate': eligibility['interest_rate'],
            'next_payment_date': payment_deadline,
            'loan_deadline': deadline
        })

    def get(self, request):
        user = request.user

        loans = self.get_queryset().filter(user=user).order_by('-created_at')
        serializer = self.serializer_class(loans, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class PaymentView(generics.ListCreateAPIView):
    """
    API endpoints for loan payments
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = PaymentDetailSerializer
    pagination_class = StandardResultsSetPagination
    queryset = LoanPayment.objects.all()

    def post(self, request, loan_id=None):
        user = request.user
        loan = Loan.objects.filter(pk=loan_id).prefetch_related('loanpayment_set')
        if not loan.exists():
            return Response({
                'detail': MESSAGES.get('NOT_FOUND').format('Loan')
            }, status=status.HTTP_404_NOT_FOUND)

        loan = loan.first()
        if not loan.user == user:
            return Response({
                'detail': MESSAGES.get('NOT_LOAN_OWNER')
            }, status=status.HTTP_400_BAD_REQUEST)

        if loan.status == 'paid':
            return Response({
                'detail': MESSAGES.get('LOAN_ALREADY_PAID')
            }, status=status.HTTP_400_BAD_REQUEST)

        payment = loan.loanpayment_set.filter(status='pending')

        if not payment.exists():
            return Response({
                'detail': MESSAGES.get('LOAN_ALREADY_PAID')
            }, status=status.HTTP_400_BAD_REQUEST)

        payment = payment.first()
        payment.payment_date = datetime.datetime.now()
        payment.status = 'paid'
        payment.save()

        loan_profile = LoanProfile.objects.filter(user=user)
        loan_profile = loan_profile.first() \
            if loan_profile.exists() \
            else LoanProfile(user=user, score=0)
        today = datetime.date.today()
        if payment.deadline < today:
            loan_profile.score -= 3
        else:
            loan_profile.score += 1
        loan_profile.save()

        total_payment = 0
        for pm in loan.loanpayment_set.all():
            total_payment += pm.amount

        serializer = self.serializer_class(payment)
        response_data = serializer.data
        if total_payment >= (loan.amount + loan.amount * loan.interest_rate / 100):
            loan.status = 'paid'
            loan.save()
        else:
            LoanPayment.objects.create(
                loan=loan,
                amount=payment.amount,
                status='pending',
                payment_date=None,
                deadline=add_months(payment.deadline, 1))

        response_data['loan_status'] = loan.status
        return Response(response_data)

    def get(self, request, loan_id=None):
        if not loan_id:
            return Response({
                'detail': MESSAGES.get('URL_PARAM_MISSING')
            }, status=status.HTTP_400_BAD_REQUEST)

        payments = self.get_queryset().filter(loan=loan_id).order_by('-created_at')
        serializer = self.serializer_class(payments, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
