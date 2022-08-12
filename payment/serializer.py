from rest_framework import serializers


def is_amount(value):
    """Checking that the value entered is a valid money amount"""
    if value <= 0:
        raise serializers.ValidationError({"detail": "Invalid Amount"})
    return value


class AcceptFundsSerializer(serializers.Serializer):
    """Serializer for sending request to Paystack"""

    amount = serializers.IntegerField(validators=[is_amount])
