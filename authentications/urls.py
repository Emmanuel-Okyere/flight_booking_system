"""User accounts urls"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentications.views import (MyTokenObtainPairView, UserDetails,
                                   UserRegistration)

urlpatterns = [
    path("register/",UserRegistration.as_view(), name="register"),
    path("user/",UserDetails.as_view(), name="details"),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
