from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.user.views import SignupView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('signup/', SignupView.as_view(), name='signup')
]
