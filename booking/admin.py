from django.contrib import admin
from booking.models import Booking

# Register your models here.
@admin.register(Booking)
class AdminBooking(admin.ModelAdmin):
    list_display = ["flight_id", "user_id", "seat_number", "payment_id"]
