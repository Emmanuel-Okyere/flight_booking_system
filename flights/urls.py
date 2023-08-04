from django.urls import path
from flights.views import AdminCreateFlight, ManagerUpdatesFlights

urlpatterns = [
    path("admin/create/", AdminCreateFlight.as_view(), name="flight_create"),
    path(
        "manager/update/<int:pk>/",
        ManagerUpdatesFlights.as_view(),
        name="flight_update",
    ),
    path(
        "manager/update/",
        ManagerUpdatesFlights.as_view(),
        name="flight_update",
    ),
]
