from rest_framework import serializers

from api.user.serializers import UserDetailSerializer
from app.models import Account, Transaction


class AccountListSerializer(serializers.ModelSerializer):
    """
    List serializer class for Account model
    """
    user = UserDetailSerializer()

    class Meta:
        model = Account
        fields = [
            'number',
            'user'
        ]


class AccountDetailSerializer(serializers.ModelSerializer):
    """
    Retrieve serializer class for Account model
    """
    user = UserDetailSerializer()

    class Meta:
        model = Account
        fields = [
            'number',
            'user',
            'balance',
            'is_active',
            'created_at'
        ]


class ActivityListSerializer(serializers.ModelSerializer):
    """
    List serializer class for Transaction model
    """
    class Meta:
        model = Transaction
        fields = [
            'id',
            'type',
            'amount',
            'description',
            'created_at'
        ]
