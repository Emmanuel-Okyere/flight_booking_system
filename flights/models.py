from django.db import models

# Create your models here.
class Flights(models.Model):
    """Flight model"""

    flight_name = models.CharField(max_length=150, null=False)
    source = models.CharField(max_length=150, null=False)
    destination = models.CharField(max_length=150, null=False)
    price_per_seat = models.DecimalField(decimal_places=2, max_digits=100)
    seats_available = models.IntegerField()
    plane_name = models.CharField(max_length=150, null=False)
    time_of_departure = models.DateTimeField()
    time_of_arrival = models.DateTimeField()
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flight_name}"
