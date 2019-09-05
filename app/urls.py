from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.account.views import AccountView, ActivityView
from api.loan.views import LoanView, PaymentView
from api.user.views import SignupView, UserInfoView


urlpatterns = [
    # Auth routes
    path('login/', obtain_auth_token, name='login'),

    # User Routes
    path('signup/', SignupView.as_view(), name='signup'),
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('user/<int:user_id>/', UserInfoView.as_view(), name='user-info'),

    # Account Routes
    path('account/', AccountView.as_view(), name='account'),
    path(
        'account/<int:account_number>/activity/',
        ActivityView.as_view(),
        name='account-activity'),

    # Loan Routes
    path('loan/', LoanView.as_view(), name='loan'),
    path(
        'loan/<int:loan_id>/payment/',
        PaymentView.as_view(),
        name='loan-payment')
]
