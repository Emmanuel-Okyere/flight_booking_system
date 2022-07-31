from rest_framework import serializers

from flights.models import Flights


class AdminCreateFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flights
        exclude = ["is_approved"]


class ManagetUpdateFLightSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField()

    class Meta:
        model = Flights
        fields = ["is_approved"]


class ManagerGetsAllFlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flights
        fields = "__all__"
