from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from booking.models import Booking
from booking.serializer import UserBookFlightSerializer, UserGetAllFlightsAvailable
from flights.models import Flights

# Create your views here.


class UserBookingView(ListAPIView):
    """User booking flight view"""

    serializer_class = UserGetAllFlightsAvailable
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Getting of all bookings in the system"""
        return Flights.objects.filter(is_approved=True)

    def post(self, request):
        serializer = UserBookFlightSerializer(data=request.data)
        try:
            if serializer.is_valid():
                flight_id = serializer.validated_data["flight_id"]
                user_id = request.user
                seat_number = serializer.validated_data["seat_number"]
                type_of_seats = serializer.validated_data["type_of_seats"]
                flight_object = Flights.objects.filter(id=flight_id.id)
                flight_get_object = Flights.objects.get(id=flight_id.id)
                try:
                    if flight_get_object.seats_available > 0:
                        booked_objects = Booking.objects.get(seat_number=seat_number)
                        return Response(
                            {"status": "failure", "detail": "seat already booked"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        return Response(
                            {"status": "failure", "detail": "All seats booked"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except Booking.DoesNotExist:
                    if flight_get_object.seats_available > 0:
                        flight_object.update(
                            seats_available=flight_get_object.seats_available - 1
                        )
                        Booking.objects.create(
                            flight_id=flight_id,
                            user_id=user_id,
                            seat_number=seat_number,
                            type_of_seats=type_of_seats,
                        )
                        return Response(
                            {
                                "status": "success",
                                "detail": "booking successful",
                                "data": {
                                    "flight": flight_id.flight_name,
                                    "user": user_id.email_address,
                                    "seat_number": seat_number,
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
