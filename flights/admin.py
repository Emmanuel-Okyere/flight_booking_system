from atexit import register
from django.contrib import admin
from flights.models import Flights

# Register your models here.


@admin.register(Flights)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("flight_name", "source", "destination", "seats_available")
