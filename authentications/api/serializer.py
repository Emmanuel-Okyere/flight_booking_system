"""Serializer class for User account"""
from rest_framework import serializers
from authentications.models import Users

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer class for registration of users"""
    class Meta:
        """Pre display all fields except password field since it is write only"""
        model = Users
        fields = ["id","first_name","last_name",
        "username","email_address","phone_number","password"]
