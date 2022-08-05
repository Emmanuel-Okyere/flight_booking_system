from django.db import models
from flights.models import Flights
from authentications.models import Users

# Create your models here.
class Booking(models.Model):
    """Flight booking model"""

    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    payment_id = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    type_of_seats = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.flight_id}"
