from rest_framework import serializers

# from api.user.serializers import UserDetailSerializer
from app.models import Loan, LoanPayment


class LoanListSerializer(serializers.ModelSerializer):
    """
    List serializer class for Loan model
    """

    class Meta:
        model = Loan
        fields = [
            'id',
            'amount',
            'interest_rate',
            'deadline'
        ]


class PaymentListSerializer(serializers.ModelSerializer):
    """
    List serializer class for Loan Payment model
    """

    class Meta:
        model = LoanPayment
        fields = [
            'id',
            'amount',
            'status',
            'payment_date',
            'deadline'
        ]
