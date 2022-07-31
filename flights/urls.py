from re import A
from django.urls import path
from flights.views import AdminCreateFlight, ManagerUpdatesFlights

urlpatterns = [
    path("create/", AdminCreateFlight.as_view(), name="flight_create"),
    path("create/<int:pk>/", ManagerUpdatesFlights.as_view(), name="flight_update"),
]
