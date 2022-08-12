from rest_framework import serializers

from booking.models import Booking


# def is_amount(value):
#     """Checking that the value entered is a valid money amount"""
#     if value <= 0:
#         raise serializers.ValidationError({"detail": "Invalid Amount"})
#     return value


class AcceptFundsSerializer(serializers.ModelSerializer):
    """Serializer for sending request to Paystack"""

    class Meta:
        model = Booking
        fields = ["flight_id"]
