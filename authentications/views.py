from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from authentications.api.serializer import RegisterSerializer
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
                "details":"user created successfully",
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
                "details":serializers.errors
            }, status=status.HTTP_400_BAD_REQUEST)

