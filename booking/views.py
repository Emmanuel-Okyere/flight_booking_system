from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentications.views import IsAdmin, IsSuperUser
from booking.models import Booking
from booking.serializer import UserBookFlightSerializer
from flights.models import Flights

# Create your views here.


class UserBookingView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = UserBookFlightSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        try:
            if serializer.is_valid():
                flight_id = serializer.data["flight_id"]
                user_id = serializer.data["user_id"]
                seat_number = serializer.data["seat_number"]
                payment_id = serializer.data["payment_id"]
                is_booked = serializer.data["is_booked"]
                type_of_seats = serializer.data["type_of_seats"]
                flight_object = Flights.objects.filter(id=flight_id)
                try:
                    booked_objects = Booking.objects.get(seat_number=seat_number)
                    return Response(
                        {"status": "failure", "detail": "seat already booked"}
                    )
                except Booking.DoesNotExist:
                    flight_get_object = Flights.objects.get(id=flight_id)
                    if flight_get_object.seats_available > 0:
                        flight_object.update(
                            seats_available=flight_get_object.seats_available - 1
                        )
                        serializer.save()
                        return Response(
                            {
                                "status": "success",
                                "detail": "booking successful",
                                "data": {
                                    "flight_id": flight_id,
                                    "user_id": user_id,
                                    "seat_number": seat_number,
                                    "payment_id": payment_id,
                                    "is_booked": is_booked,
                                    "type_of_seats": type_of_seats,
                                    "seats_available": flight_get_object.seats_available
                                    - 1,
                                },
                            },
                            status=status.HTTP_201_CREATED,
                        )
                    else:
                        return Response(
                            {"status": "failure", "detail": "All seats booked"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {"status": "failure", "detail": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Flights.DoesNotExist:
            return Response(
                {"status": "failure", "detail": "flight not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
