"""User accounts urls"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentications.views import (
    UserLogin,
    UserDetails,
    UserRegistration,
    EmailVerification,
    ChangePassword,
    RequestResetPasswordEmail,
    ResetPasswordLinkVerify,
    ResetPasswordView,
    ManagerRegisterUserView,
    GoogleLoginView,
    UserLogOut,
)


urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path("register-admin/", ManagerRegisterUserView.as_view(), name="register_admin"),
    path("user/", UserDetails.as_view(), name="details"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogOut.as_view(), name="logout"),
    path("verify-email/", EmailVerification.as_view(), name="email_verify"),
    path("change-password/", ChangePassword.as_view(), name="change_password"),
    path("reset-password/", RequestResetPasswordEmail.as_view(), name="reset-password"),
    path(
        "reset-password/confirm/",
        ResetPasswordLinkVerify.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "reset-password/done/", ResetPasswordView.as_view(), name="reset-password-done"
    ),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("google/", GoogleLoginView.as_view(), name="google"),
]
