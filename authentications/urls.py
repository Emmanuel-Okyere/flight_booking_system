"""User accounts urls"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentications.views import (UserLogin, UserDetails,
                                   UserRegistration,EmailVerification)

urlpatterns = [
    path("register/",UserRegistration.as_view(), name="register"),
    path("user/",UserDetails.as_view(), name="details"),
    path("verify-email/",EmailVerification.as_view(), name="details"),
    path('login/', UserLogin.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
