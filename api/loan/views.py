import datetime
import math

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.loan.serializers import LoanListSerializer, PaymentListSerializer
from app.constants import MESSAGES
from app.core.paginations import StandardResultsSetPagination
from app.helpers import add_months, is_eligible_lender
from app.models import Loan, LoanProfile, LoanPayment


class LoanView(generics.ListCreateAPIView):
    """
    API Endpoints for loan
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = LoanListSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Loan.objects.all()

    def post(self, request):
        user = request.user
        requested_amount = request.data.get('amount')
        requested_length = request.data.get('length')

        errors = {}

        if not requested_amount:
            errors['amount'] = [MESSAGES.get('')]

        if not requested_length:
            errors['length'] = [MESSAGES.get('')]

        loan_profile = LoanProfile.objects.filter(user=user)
        if loan_profile.exists():
            loan_profile = loan_profile.first()
            loan_finished = True
            loans = self.get_queryset().prefetch_related('loanpayment_set').filter(user=user)

            for loan in loans:
                total_amount = loan.amount + (loan.amount * loan.interest_rate / 100)
                amount = 0
                for payment in loan.loanpayments_set.all():
                    amount += payment.amount

                if total_amount > amount:
                    loan_finished = False

            if not loan_finished:
                return Response({
                    'detail': MESSAGES.get('')
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
    serializer_class = PaymentListSerializer
    pagination_class = StandardResultsSetPagination
    queryset = LoanPayment.objects.all()

    def post(self, request, loan_id=None):
        user = request.user
        loan = Loan.objects.filter(pk=loan_id).prefetch_related('loanpayment_set')
        if not loan.exists():
            return Response({
                'detail': MESSAGES.get('')
            }, status=status.HTTP_404_NOT_FOUND)

        loan = loan.first()
        if not loan.user == user:
            return Response({
                'detail': MESSAGES.get('')
            }, status=status.HTTP_400_BAD_REQUEST)

        payment = loan.loanpayment_set.filter(status='pending')

        if payment.exists():
            payment = payment.first()
            payment.payment_date = datetime.date.today()
            payment.status = 'paid'
            payment.save()

        LoanPayment.objects.create(
            loan=loan,
            amount=payment.amount,
            status='pending',
            payment_date=None,
            deadline=add_months(payment.deadline))

    def get(self, request, loan_id=None):
        if not loan_id:
            return Response({
                'detail': MESSAGES.get('')
            }, status=status.HTTP_400_BAD_REQUEST)

        payments = self.get_queryset().filter(loan=loan_id)
        serializer = self.serializer_class(payments, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
