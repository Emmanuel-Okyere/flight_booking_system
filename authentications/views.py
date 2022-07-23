"""VIews for Authentications application"""
import os
from rest_framework import status
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from authentications.api.serializer import (MyTokenObtainPairSerializer,
                                            RegisterSerializer,
                                            UserDetailSerializer)
from authentications.models import Users

# Create your views here.
class UserRegistration(GenericAPIView):
    """User resgistration view class"""
    queryset = Users.objects
    serializer_class = RegisterSerializer
    permission_classes = []
    authentication_classes = []
    def post(self,request):
        """Post request for user registration"""
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            self.queryset.create_user(**serializers.data)
            user = self.queryset.get(email_address=serializers.data["email_address"])
            email = serializers.data["email_address"]
            confirmation_token = default_token_generator.make_token(user)
            send_mail("Email Verification Link",
                f"Email Verification link:{os.getenv('VERIFY_HOSTNAME')}accounts/verify-email/?iam={email}&def={confirmation_token}\n\n\n\n\n\n Do not share this link with anyone.\n This link can only be used once",
                os.getenv("EMAIL_HOST_USER"), [email])
            return Response({
                "status":"sucess",
                "detail":"user created successfully",
                "data":{
                    "first_name":serializers.data["first_name"],
                    "last_name":serializers.data["last_name"],
                    "email_address":email,
                    "username":serializers.data["username"]
                }
            },status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status":"failure",
                "detail":serializers.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(GenericAPIView):
    """Email Verification"""
    queryset = Users.objects
    def get(self, request):
        """Getting the token and email from user verification link"""
        try:
            user = self.queryset.get(email_address =request.GET["iam"])
            token = request.GET["def"]
            if default_token_generator.check_token(user,token):
                if user.is_active:
                    return Response({
                        "status":"failure",
                        "detail":"email already verified",
                    }, status=status.HTTP_403_FORBIDDEN)
                else:
                    user.is_active = True
                    user.save()
                    return Response({
                        "status":"sucess",
                        "detail":"email verified successful",
                        "data":{
                            "is_active":user.is_active
                        }
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status":"failure",
                    "detail":"link invalid"
                }, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({
                    "status":"failure",
                    "detail":"User with link does not exist"
                }, status=status.HTTP_200_OK)


class UserLogin(TokenObtainPairView):
    """Overiding the TokenObtainPiarView of simple jwt to login user"""
    serializer_class = MyTokenObtainPairSerializer



class UserDetails(GenericAPIView):
    """View for getting user details with tokens"""
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        """Get function request"""
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response({
            "status":"success",
            "detail": "User details found",
            "data":{
                "id":serializer.data["id"],
                "first_name":serializer.data["first_name"],
                "last_name":serializer.data["last_name"],
                "username":serializer.data["username"],
                "email_address":serializer.data["email_address"],
                "phone_number":serializer.data["phone_number"],
                "is_admin":serializer.data["is_admin"],
                "is_superuser":serializer.data["is_superuser"],
                }})
