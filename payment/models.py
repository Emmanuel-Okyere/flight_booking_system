from django.db import models
from authentications.models import Users

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(Users, null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, default="GHS")
    created_at = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return f"{self.user.__str__()}"


class Payment(models.Model):
    TRANSACTION_TYPES = (
        (0, "deposit"),
        (1, "transfer"),
        (2, "withdraw"),
    )
    STATUS = (
        (0, "paid"),
        (1, "pending"),
        (2, "not sucess"),
    )
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=200, null=True, choices=TRANSACTION_TYPES
    )
    receipt = models.IntegerField()
    amount_credited = models.DecimalField(decimal_places=2, max_digits=200)
    customer_name = models.CharField(max_length=250)
    customer_number = models.IntegerField()
    payment_status = models.CharField(
        max_length=200, null=True, choices=STATUS, default="pending"
    )
    paystack_payment_reference = models.CharField(
        max_length=100, default="", blank=True
    )

    def __str__(self):
        return f"{self.wallet.user.__str__()}"
