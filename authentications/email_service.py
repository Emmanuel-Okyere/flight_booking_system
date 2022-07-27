import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def custom_send_email(email, confirmation_token):
    """Sending email service"""
    from_email = os.getenv("EMAIL_HOST_USER")
    subject = "Email Verification Link"
    mail_body = render_to_string(
        "send_email.html",
        {"email_address": email, "confirmation_token": confirmation_token},
    )
    plain_message = strip_tags(mail_body)
    send_mail(subject, plain_message, from_email, [email], html_message=mail_body)
