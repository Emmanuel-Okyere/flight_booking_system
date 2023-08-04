"""Payment and Verification view"""
import requests

from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from booking.models import Booking
from payment.serializer import AcceptFundsSerializer

from payment.models import Payment


class AcceptFunds(APIView):
    """Accepting Funds after user makes the payment"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Post request for making payments"""
        serializer = AcceptFundsSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.data)
            flight_object = serializer.validated_data["flight_id"]
            try:
                booking = Booking.objects.filter(user_id=request.user)
                if booking[0].is_booked:
                    return Response(
                        {"status": "failure", "detail": "payment already made"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    user = self.request.user
                    serializer.validated_data["amount"] = (
                        flight_object.price_per_seat * len(booking)
                    ) * 100
                    serializer.validated_data["email"] = user.email_address
                    data = serializer.validated_data
                    url = "https://api.paystack.co/transaction/initialize"
                    headers = {
                        "authorization": f"Bearer {settings.PAYSTACK_TEST_SECRET}"
                    }
                    r = requests.post(url, headers=headers, data=data)
                    response = r.json()
                    Payment.objects.create(
                        amount_credited=serializer.validated_data["amount"],
                        paystack_payment_reference=response["data"]["reference"],
                        payment_status=1,
                    )
                    return Response(
                        {
                            "status": "sucess",
                            "detail": "Authorization URL created",
                            "data": {
                                "authorization_url": response["data"][
                                    "authorization_url"
                                ],
                                "access_code": response["data"]["access_code"],
                                "reference": response["data"]["reference"],
                            },
                        },
                        status=status.HTTP_201_CREATED,
                    )

            except Booking.DoesNotExist:
                return Response({"status": "failure", "detail": "Booking not found"})
        else:
            return Response(
                {"status": "sucess", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyFunds(APIView):
    """View for verification of the payment made by the user"""

    permission_classes = [IsAuthenticated]

    def get(self, request, reference):
        """Verifying payement refrence from paystack"""
        try:
            transaction = Payment.objects.get(paystack_payment_reference=reference)
            booking = Booking.objects.filter(user_id=request.user)
            reference = transaction.paystack_payment_reference
            url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {"authorization": f"Bearer {settings.PAYSTACK_TEST_SECRET}"}
            r = requests.get(url, headers=headers)
            resp = r.json()
            if resp["data"]["status"] == "success":
                payment_status = 0
                amount = (resp["data"]["amount"]) / 100
                Payment.objects.filter(paystack_payment_reference=reference).update(
                    receipt=resp["data"]["id"],
                    payment_status=payment_status,
                    amount_credited=amount,
                    customer_number=resp["data"]["customer"]["customer_code"],
                )
                booking.update(payment_id=transaction.id, is_booked=True)
                return Response(
                    {
                        "status": "sucess",
                        "detail": "Verification successful",
                        "data": {
                            "receipt_id": resp["data"]["id"],
                            "payment_status": "paid",
                            "amount_credited": amount,
                            "customer_number": resp["data"]["customer"][
                                "customer_code"
                            ],
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"status": "failure", "detail": "payment uncessful"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Payment.DoesNotExist:
            return Response(
                {
                    "status": "failure",
                    "detail": "Payment with that code does not exits",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Booking.DoesNotExist:
            return Response(
                {"status": "failure", "detail": "must book flight first"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Create your views here.
