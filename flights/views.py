from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from flights.models import Flights
from flights.serializer import AdminCreateFlightSerializer

# Create your views here.
class AdminCreateFlight(ListAPIView):
    queryset = Flights.objects.all()
    serializer_class = AdminCreateFlightSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

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
