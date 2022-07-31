from rest_framework import serializers

from flights.models import Flights


class AdminCreateFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flights
        fields = "__all__"


class ManagetUpdateFLightSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField()

    class Meta:
        model = Flights
        fields = ["is_approved"]
