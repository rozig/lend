from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.user.serializers import UserSerializer, UserDetailSerializer
from app.constants import MESSAGES
from app.helpers import generate_account_number
from app.models import Account, Loan, LoanProfile, User


class SignupView(APIView):
    """
    API Endpoint for user signup
    """
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.data, password=request.data.get('password'))

        account_number = generate_account_number()
        Account.objects.create(number=account_number, user=user)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class UserInfoView(APIView):
    """
    API Endpoint for user information
    """
    serializer_class = UserDetailSerializer

    def get(self, request, user_id=None):
        user = request.user
        if user_id:
            user = User.objects.filter(pk=user_id).first()

        if not user:
            return Response({
                'detail': MESSAGES.get('NOT_FOUND').format('user')
            }, status=status.HTTP_404_NOT_FOUND)

        loan_profile = LoanProfile.objects.filter(user=user)
        num_of_loans = len(Loan.objects.filter(user=user))

        serializer = self.serializer_class(user)
        response_data = serializer.data
        response_data['lend_score'] = loan_profile.first().score \
            if loan_profile.exists() else None
        response_data['num_of_loans'] = num_of_loans
        return Response(response_data)
