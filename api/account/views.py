from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.account.serializers import AccountDetailSerializer, ActivityListSerializer
from app.constants import MESSAGES
from app.core.paginations import StandardResultsSetPagination
from app.helpers import generate_account_number
from app.models import Account, Transaction


class AccountView(APIView):
    """
    API Endpoints for account
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = AccountDetailSerializer

    def post(self, request):
        user = request.user

        account = Account.objects.filter(user=user)
        if account.exists():
            return Response({
                'detail': MESSAGES.get('ACCOUNT_EXISTS')
            }, status=status.HTTP_400_BAD_REQUEST)

        account_number = generate_account_number()
        account = Account.objects.create(
            number=account_number,
            user=user)
        serializer = self.serializer_class(account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user

        account = Account.objects.filter(user=user)
        if not account.exists():
            return Response({
                'detail': MESSAGES.get('ACCOUNT_DOES_NOT_EXIST')
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(account.first())
        return Response(serializer.data)


class ActivityView(generics.ListAPIView):
    """
    List API Endpoint for account activities
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = ActivityListSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Transaction.objects.all()

    def get(self, request, account_number=None):
        if not account_number:
            return Response({
                'detail': MESSAGES.get('URL_PARAM_MISSING')
            }, status=status.HTTP_400_BAD_REQUEST)

        transactions = self.get_queryset().filter(account=account_number)
        serializer = self.serializer_class(transactions, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
