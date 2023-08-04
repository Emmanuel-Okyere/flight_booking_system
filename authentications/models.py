"""Models for user creation"""
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
class FlightManager(BaseUserManager):
    """Registration of the user using the BaseUserManager to create a superuser"""

    def create_user(
        self,
        email_address,
        username=None,
        password=None,
        first_name=None,
        last_name=None,
        phone_number=None,
    ):
        """Creation of user"""
        if not email_address:
            raise ValueError("user must have email address")

        user = self.model(
            email_address=email_address,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(
        self, email_address, password, username=None, first_name=None, last_name=None
    ):
        """Creation of the admin user"""
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email_address=email_address,
            password=password,
        )
        user.is_changed_password = False
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password, username=None):
        """Creation of a superuser"""
        user = self.create_user(
            username=username, email_address=email_address, password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    """User creation model"""

    first_name = models.CharField(max_length=200, blank=False, null=True)
    last_name = models.CharField(max_length=200, blank=False, null=True)
    email_address = models.EmailField(verbose_name="email", unique=True, max_length=200)
    username = models.CharField(max_length=200, blank=False, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_changed_password = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["username"]
    objects = FlightManager()

    class Meta:
        """Pre displayed field"""

        ordering = ("email_address",)

    def __str__(self):
        return f"{self.email_address}"

    def has_perm(self, perm, obj=None):
        """When user registraion has permission, then it is a superuser"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Has permission to access the model, like create a super user"""
        return self.is_superuser
