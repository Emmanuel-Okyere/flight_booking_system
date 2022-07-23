"""Serializer class for User account"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authentications.models import Users

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer class for registration of users"""
    class Meta:
        """Pre display all fields except password field since it is write only"""
        model = Users
        fields = ["id","first_name","last_name",
        "username","email_address","phone_number","password"]
class ChangePasswordSerializer(serializers.ModelSerializer):
    """User change password serializer"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        """Pre displayed fields for user"""
        model = Users
        fields = [
            "old_password",
            "new_password"
        ]

class UserDetailSerializer(serializers.ModelSerializer):
    """Verifying user tokens to get details"""
    class Meta:
        model = Users
        fields = ["id","first_name","last_name",
        "username","email_address","phone_number","is_admin","is_superuser"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Overiding of TokenPairSerialier class"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['email_address'] = user.email_address
        token['phone_number'] = user.phone_number
        token['is_admin'] = user.is_admin
        token['is_superuser'] = user.is_superuser

        return token
