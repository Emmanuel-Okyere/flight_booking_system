from rest_framework.exceptions import APIException


class FlightNotFound(APIException):
    """Exception for when a user does not exist"""

    status_code = 404
    default_detail = {"status": "failure", "detail": "flight object does not exits"}
