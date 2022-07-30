from re import A
from django.urls import path, include
from flights.views import AdminCreateFlight

urlpatterns = [
    path("create/", AdminCreateFlight.as_view(), name="flight_create"),
    # path("flight/", include("flights.urls"), name="flights"),
]
