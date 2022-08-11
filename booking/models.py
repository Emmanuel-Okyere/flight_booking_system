from django.db import models
from flights.models import Flights
from authentications.models import Users
from payment.models import Payment

# Create your models here.
class Booking(models.Model):
    """Flight booking model"""

    SEAT_TYPES = (
        (0, "first class"),
        (1, "business"),
        (2, "economy"),
    )
    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    seat_number = models.IntegerField(default=1)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    is_booked = models.BooleanField(default=False)
    type_of_seats = models.CharField(max_length=200, null=True, choices=SEAT_TYPES)

    def __str__(self):
        return f"{self.flight_id}"
