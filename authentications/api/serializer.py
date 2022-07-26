"""Serializer class for User account"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authentications.models import Users
from rest_framework.exceptions import NotAuthenticated


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer class for registration of users"""

    class Meta:
        """Pre display all fields except password field since it is write only"""

        model = Users
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email_address",
            "phone_number",
            "password",
        ]

    def validate(self, attrs):
        if len(attrs["password"]) < 8:
            raise serializers.ValidationError(
                {"password": "password must be 8 characters or more"}
            )
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.ModelSerializer):
    """User change password serializer"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        """Pre displayed fields for user"""

        model = Users
        fields = ["old_password", "new_password"]

    def validate(self, attrs):
        if len(attrs["new_password"]) < 8:
            raise serializers.ValidationError(
                {"password": "password must be 8 characters or more"}
            )
        return super().validate(attrs)


class RequestPasswordResetEmail(serializers.ModelSerializer):
    email_address = serializers.EmailField()

    class Meta:
        model = Users
        fields = ["email_address"]


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    email_address = serializers.EmailField()
    token = serializers.CharField()

    class Meta:
        model = Users
        fields = ["password", "email_address", "token"]


class UserDetailSerializer(serializers.ModelSerializer):
    """Verifying user tokens to get details"""

    class Meta:
        model = Users
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email_address",
            "phone_number",
            "is_admin",
            "is_superuser",
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Overiding of TokenPairSerialier class"""

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["data"] = {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "username": self.user.username,
            "email_address": self.user.email_address,
            "phone_number": self.user.phone_number,
            "is_admin": self.user.is_admin,
            "is_superuser": self.user.is_superuser,
        }

        if not self.user.is_changed_password:
            raise NotAuthenticated(
                {
                    "message": "You are required to change your password",
                    "access": str(refresh.access_token),
                }
            )

        return data


class ManagerRegisterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["username", "first_name", "last_name", "email_address"]
