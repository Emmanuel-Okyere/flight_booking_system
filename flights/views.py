"""FLight booking view file"""
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentications.views import IsAdmin, IsSuperUser
from flights.models import Flights
from flights.serializer import (
    AdminCreateFlightSerializer,
    ManagetUpdateFLightSerializer,
    ManagerGetsAllFlightsSerializer,
)
from flights.exceptions import FlightNotFound

# Create your views here.


class AdminCreateFlight(ListAPIView):
    """Admin creating flight view"""

    queryset = Flights.objects.all()
    serializer_class = AdminCreateFlightSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def post(self, request):
        """Post request to create new flight"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = self.queryset.create(**serializer.data)
            data.save()
            return Response(
                {
                    "status": "success",
                    "detail": "flight created",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ManagerUpdatesFlights(ListAPIView, RetrieveAPIView):
    """Manager approving upfated by the admin users"""

    queryset = Flights.objects.all()
    serializer_class = ManagerGetsAllFlightsSerializer
    permission_classes = (IsAuthenticated, IsSuperUser)

    def patch(self, request, pk):
        """Patch request to update the fields"""
        try:
            flight_object = Flights.objects.get(pk=pk)
            serializer = ManagetUpdateFLightSerializer(flight_object, request.data)
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
            return Response(
                {"status": "failure", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Flights.DoesNotExist as exc:
            raise FlightNotFound from exc

    def delete(self, request, pk):
        """Delete method to delete an object from the database"""
        try:
            flight_object = Flights.objects.get(pk=pk)
            flight_object.delete()
            return Response(
                {"status": "sucess", "detail": "flight delete success"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Flights.DoesNotExist as exc:
            raise FlightNotFound from exc
