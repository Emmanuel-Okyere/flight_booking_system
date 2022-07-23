"""Admin registration of user model"""
from django.contrib import admin
from authentications.models import Users
# Register your models here.

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    """User Admin class"""
    list_display = ("username","first_name","last_name","email_address")
