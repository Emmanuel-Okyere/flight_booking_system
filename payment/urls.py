"""Urls for payement views"""
from django.urls import path
from payment.views import AcceptFunds, VerifyFunds

urlpatterns = [
    path("accept/", AcceptFunds.as_view()),
    path("accept/verify/<str:reference>/", VerifyFunds.as_view()),
]
