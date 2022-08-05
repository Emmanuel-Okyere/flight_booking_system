from django.urls import path
from booking.views import UserBookingView

urlpatterns = [
    path("create/", UserBookingView.as_view(), name="booking_create"),
]
