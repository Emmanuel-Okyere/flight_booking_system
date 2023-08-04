from rest_framework import serializers
from booking.models import Booking
from flights.models import Flights


class UserBookFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ["user_id", "is_booked"]


class UserGetAllFlightsAvailable(serializers.ModelSerializer):
    class Meta:
        model = Flights
        exclude = ["is_approved", "created", "updated"]
