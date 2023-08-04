from django.db import models

# Create your models here.


class Payment(models.Model):
    STATUS = (
        (0, "paid"),
        (1, "pending"),
        (2, "failed"),
    )

    receipt = models.IntegerField(null=True)
    amount_credited = models.DecimalField(decimal_places=2, max_digits=200)
    customer_name = models.CharField(max_length=250, null=True)
    customer_number = models.CharField(max_length=250, null=True)
    payment_status = models.CharField(
        max_length=200, null=True, choices=STATUS, default="pending"
    )
    paystack_payment_reference = models.CharField(
        max_length=100, default="", blank=True
    )

    def __str__(self):
        return f"{self.paystack_payment_reference}"
