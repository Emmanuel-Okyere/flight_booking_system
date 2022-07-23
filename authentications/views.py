"""VIews for Authentications application"""
from rest_framework import status
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

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
            return Response({
                "status":"sucess",
                "detail":"user created successfully",
                "data":{
                    "first_name":serializers.data["first_name"],
                    "last_name":serializers.data["last_name"],
                    "email_address":serializers.data["email_address"],
                    "username":serializers.data["username"]
                }
            },status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status":"failure",
                "detail":serializers.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    """Overiding the TokenObtainPiarView of simple jwt"""
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
