"""VIews for Authentications application"""
import random
import string
import requests
from rest_framework.utils import json
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from requests.exceptions import ConnectionError
from authentications.api.serializer import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UserDetailSerializer,
    ChangePasswordSerializer,
    RequestPasswordResetEmail,
    ResetPasswordSerializer,
    ManagerRegisterAdminSerializer,
)
from authentications.models import Users
from authentications.exceptions import UserNotFound, InvalidLink
from authentications.email_service import (
    send_email_verification_mail,
    send_reset_password_email,
    send_admin_login_credentials_email,
)

# Create your views here.
class IsSuperUser(IsAdminUser):
    """Checking to see if the current user is Admin user authentication"""

    def has_permission(self, request, view):
        """When called, gives the user permissions to some views"""
        return bool(request.user and request.user.is_superuser)


class IsAdmin(IsAdminUser):
    """Checking to see if the current user is Admin user authentication"""

    def has_permission(self, request, view):
        """When called, gives the user permissions to some views"""
        return bool(request.user and request.user.is_superuser is False)


class UserRegistration(GenericAPIView):
    """User resgistration view class"""

    queryset = Users.objects
    serializer_class = RegisterSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """Post request for user registration"""
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            self.queryset.create_user(**serializers.data)
            user = self.queryset.get(email_address=serializers.data["email_address"])
            email = serializers.data["email_address"]
            first_name = user.first_name
            confirmation_token = default_token_generator.make_token(user)
            send_email_verification_mail(
                first_name=first_name, email=email, token=confirmation_token
            )
            return Response(
                {
                    "status": "sucess",
                    "detail": "user created successfully",
                    "data": {
                        "first_name": serializers.data["first_name"],
                        "last_name": serializers.data["last_name"],
                        "email_address": email,
                        "username": serializers.data["username"],
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EmailVerification(GenericAPIView):
    """Email Verification"""

    serializer_class = ChangePasswordSerializer
    queryset = Users.objects

    def get(self, request):
        """Getting the token and email from user verification link"""
        try:
            user = self.queryset.get(email_address=request.GET["iam"])
            token = request.GET["def"]
            if default_token_generator.check_token(user, token):
                if user.is_active:
                    return Response(
                        {
                            "status": "failure",
                            "detail": "email already verified",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
                else:
                    user.is_active = True
                    user.save()
                    return Response(
                        {
                            "status": "sucess",
                            "detail": "email verified successful",
                            "data": {"is_active": user.is_active},
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                raise InvalidLink
        except Users.DoesNotExist as exc:
            raise UserNotFound from exc


class UserLogin(TokenObtainPairView):
    """Overiding the TokenObtainPiarView of simple jwt to login user"""

    serializer_class = MyTokenObtainPairSerializer


class ChangePassword(GenericAPIView):
    """User change password view endpoint where both users can change their password"""

    model = Users
    queryset = Users.objects
    serializer_class = ChangePasswordSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        """Making a PUT request to change passowrd by both user and superuser"""
        user = self.queryset.get(email_address=request.user)
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                if not user.check_password(serializer.data.get("old_password")):
                    return Response(
                        {
                            "status": "failure",
                            "detail": "wrong old password",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.set_password(serializer.data.get("new_password"))
                user.is_changed_password = True
                user.save()
                return Response(
                    {
                        "status": "success",
                        "detail": "Password changed successfully",
                        "data": {
                            "username": user.username,
                            "email_address": user.email_address,
                            "is_admin": user.is_staff,
                            "is_superuser": user.is_superuser,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"status": "failure", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except KeyError:
            return Response(
                {"status": "failure", "detail": "change password failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLogOut(GenericAPIView):
    """Logout API view to blacklist refresh token"""

    serializer_class = MyTokenObtainPairSerializer
    queryset = Users.objects
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Reseting refresh token to blacklist it from getting new token"""
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"status": "success", "detail": "logout successful"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except KeyError:
            return Response(
                {"status": "failure", "detail": "Logout Unsuccessful"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestResetPasswordEmail(GenericAPIView):
    """VIew for user to request password change email"""

    queryset = Users.objects
    serializer_class = RequestPasswordResetEmail
    permission_classes = []

    def post(self, request):
        """Post request to this view"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.data["email_address"]
                user = self.queryset.get(email_address=email)
                password_reset_token = default_token_generator.make_token(user)
                first_name = user.first_name
                send_reset_password_email(
                    first_name=first_name, email=email, token=password_reset_token
                )
                return Response({"status": "sucess", "detail": "reset email sent"})
            except Users.DoesNotExist as exc:
                raise UserNotFound from exc
        return Response(
            {"status": "failure", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResetPasswordLinkVerify(GenericAPIView):
    """Verification of the link sent to user when they try to access the link"""

    queryset = Users.objects
    serializer_class = RequestPasswordResetEmail
    permission_classes = []

    def get(self, request):
        """A get request with query parameters"""
        try:
            user = self.queryset.get(email_address=request.GET["iam"])
            token = request.GET["def"]
            if default_token_generator.check_token(user, token):
                return Response(
                    {
                        "status": "sucess",
                        "detail": "link verified successful",
                        "data": {"email_address": user.email_address},
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                raise InvalidLink
        except Users.DoesNotExist as exc:
            raise UserNotFound from exc


class ResetPasswordView(GenericAPIView):
    """The actual reset password view where the user enters the password"""

    queryset = Users.objects
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request):
        """Post request with link token, password and email address"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.data["email_address"]
                token = serializer.data["token"]
                password = serializer.data["password"]
                user = self.queryset.get(email_address=email)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return Response(
                        {"status": "success", "detail": "Password reset successful"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"status": "failure", "detail": "token invalid"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Users.DoesNotExist as exc:
                raise UserNotFound from exc
        return Response(
            {"status": "failure", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserDetails(GenericAPIView):
    """View for getting user details with tokens"""

    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get function request"""
        user = request.user
        serializer = self.serializer_class(user)
        return Response(
            {
                "status": "success",
                "detail": "User details found",
                "data": {
                    "id": serializer.data["id"],
                    "first_name": serializer.data["first_name"],
                    "last_name": serializer.data["last_name"],
                    "username": serializer.data["username"],
                    "email_address": serializer.data["email_address"],
                    "phone_number": serializer.data["phone_number"],
                    "is_admin": serializer.data["is_admin"],
                    "is_superuser": serializer.data["is_superuser"],
                },
            }
        )


class ManagerRegisterUserView(GenericAPIView):
    """View for Managers to create admin users"""

    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    def generate_random_password(self):
        """Generate random alphanumeric passwords for new user to be changed afterwards"""
        length = 25
        random.shuffle(self.characters)
        password = []
        for _ in range(length):
            password.append(random.choice(self.characters))
        random.shuffle(password)
        return "".join(password)

    queryset = Users.objects
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = ManagerRegisterAdminSerializer

    def post(self, request):
        """Post request to create the admin user and set the password is changed fields to false"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = self.generate_random_password()
            self.queryset.create_admin(**serializer.data, password=password)
            email = serializer.data["email_address"]
            first_name = serializer.data["first_name"]
            send_admin_login_credentials_email(
                first_name=first_name, email=email, password=password
            )
            return Response(
                {
                    "status": "success",
                    "detail": "Admin registered successfully",
                    "data": {
                        "first_name": serializer.data["first_name"],
                        "last_name": serializer.data["last_name"],
                        "username": serializer.data["username"],
                        "email_address": serializer.data["email_address"],
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GoogleLoginView(GenericAPIView):
    """Google Auth2 login view"""

    serializer_class = MyTokenObtainPairSerializer
    queryset = Users.objects
    permission_classes = []

    def post(self, request):
        """Post request to google to authenticate the token"""
        payload = {"access_token": request.data.get("token")}
        try:
            auth_request = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo", params=payload
            )
            data = json.loads(auth_request.text)
            if "error" in data:

                return Response(
                    {
                        "status": "failure",
                        "detail": "wrong google token / this google token is already expired.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ConnectionError:
            return Response(
                {
                    "status": "failure",
                    "detail": "token verification failed, please check connection",
                },
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )
        try:
            user = self.queryset.get(email_address=data["email"])
        except Users.DoesNotExist:
            try:
                first_name = data["name"].split()[0]
                last_name = data["name"].split()[-1]
                username = f"{first_name}{last_name.capitalize()}"
                user = self.queryset.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email_address=data["email"],
                    password=make_password(BaseUserManager().make_random_password()),
                )
            except KeyError:
                user = self.queryset.create_user(
                    username=data["email"],
                    email_address=data["email"],
                    password=make_password(BaseUserManager().make_random_password()),
                )
            user.is_active = True
            user.save()
        token = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(token),
                "access": str(token.access_token),
                "data": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email_address": user.email_address,
                    "phone_number": user.phone_number,
                    "is_admin": user.is_admin,
                    "is_superuser": user.is_superuser,
                },
            },
            status=status.HTTP_200_OK,
        )
