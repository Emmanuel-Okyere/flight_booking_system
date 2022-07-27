import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

FROM_EMAIL = os.getenv("EMAIL_HOST_USER")
HOST_LINK = os.getenv("VERIFY_HOSTNAME")


def send_email_verification_mail(email, token):
    """Sending email service"""
    from_email = FROM_EMAIL
    link = f"{HOST_LINK}/accounts/verify-email/?iam={email}&def={token}"
    subject = "Email Verification Link"
    mail_body = render_to_string(
        "email_verification.html",
        {"email_address": email, "confirm_link": link},
    )
    plain_message = strip_tags(mail_body)
    send_mail(subject, plain_message, from_email, [email], html_message=mail_body)


def send_reset_password_email(email, token):
    """Sending email service"""
    from_email = FROM_EMAIL
    link = f"{HOST_LINK}accounts/reset-password/confirm/?iam={email}&def={token}"
    subject = "Password Reset Confirmation"
    mail_body = render_to_string(
        "password_reset_request_email.html",
        {"email_address": email, "confirm_link": link},
    )
    plain_message = strip_tags(mail_body)
    send_mail(subject, plain_message, from_email, [email], html_message=mail_body)


def send_admin_login_credentials_email(email, password):
    """Sending email service"""
    from_email = FROM_EMAIL
    subject = "Account Creation Credentials"
    mail_body = render_to_string(
        "admin_users_email.html",
        {"email_address": email, "password": password},
    )
    plain_message = strip_tags(mail_body)
    send_mail(subject, plain_message, from_email, [email], html_message=mail_body)
