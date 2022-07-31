from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from flights.models import Flights
from flights.serializer import (
    AdminCreateFlightSerializer,
    ManagetUpdateFLightSerializer,
)
from flights.exceptions import FlightNotFound

# Create your views here.
class IsAdmin(IsAdminUser):
    """Checking to see if the current user is Admin user authentication"""

    def has_permission(self, request, view):
        """When called, gives the user permissions to some views"""
        return bool(request.user and request.user.is_superuser is False)


class AdminCreateFlight(ListAPIView):
    queryset = Flights.objects.all()
    serializer_class = AdminCreateFlightSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = self.queryset.create(**serializer.data)
            data.save()
            return Response(
                {
                    "status": "success",
                    "detail": "flight created",
                    "data": serializer.data,
                }
            )
        return Response(
            {"status": "failure", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ManagerUpdatesFlights(RetrieveAPIView):
    queryset = Flights.objects.all()
    serializer_class = ManagetUpdateFLightSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def patch(self, request, pk):
        try:
            flight_object = Flights.objects.get(pk=pk)
            serializer = self.serializer_class(flight_object, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": "sucess",
                        "detail": "flight update success",
                        "data": {
                            "flight_id": flight_object.id,
                            "price_per_seat": flight_object.price_per_seat,
                            "is_approved": flight_object.is_approved,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            return Response({"status": "failure", "detail": serializer.errors})
        except Flights.DoesNotExist as exc:
            raise FlightNotFound from exc

    def delete(self, request, pk):
        try:
            flight_object = Flights.objects.get(pk=pk)
            flight_object.delete()
            return Response(
                {"status": "sucess", "detail": "flight delete success"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Flights.DoesNotExist as exc:
            raise FlightNotFound from exc
