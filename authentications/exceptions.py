from rest_framework.exceptions import APIException


class UserNotFound(APIException):
    """Exception for when a user does not exist"""

    status_code = 404
    default_detail = {"status": "failure", "detail": "User does not exist"}


class InvalidLink(APIException):
    """Invalid link exception"""

    status_code = 400
    default_detail = {"status": "failure", "detail": "link invalid"}
