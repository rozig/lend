from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.account.serializers import (
    AccountSerializer, AccountListSerializer, AccountDetailSerializer)
from app.core.viewsets import ViewSet
from app.models import Account


class AccountViewSet(ViewSet):
    """
    API Endpoints for account management
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = AccountSerializer
    list_serializer_class = AccountListSerializer
    retrieve_serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()
