"""Test cases for authentication application"""
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from authentications.models import Users


# Create your tests here.
class TestSetup(APITestCase):
    """Setup class for the test cases"""

    def setUp(self):
        """Setup of the test"""
        self.register_url = "/accounts/register/"
        self.login_url = "/accounts/login/"
        self.admin_register_url = "/accounts/register-admin/"
        self.user = Users.objects.create_superuser(
            username="admin", email_address="admin@admin.com", password="admin1234"
        )
        self.token = RefreshToken.for_user(self.user)
        return super().setUp()


class TestUserRegistration(TestSetup):
    """Api test for user registration"""

    def test_user_can_register(self):
        """Test to see if user can register"""
        register_url = self.register_url
        data = {
            "email_address": "test1@gmail.com",
            "username": "test1",
            "password": "test1234",
        }
        response = self.client.post(register_url, data, format="json")
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 201)


class TestUserLogin(TestSetup):
    """Api test for user login"""

    def test_not_active_or_not_registered_user_cannot_login(self):
        """Test to check that users that are not active or not registered
        can not login into the system"""
        res = self.client.post(
            self.login_url,
            {
                "email_address": "test1@gmail.com",
                "password": "test1234",
            },
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_active_and_validated_users_can_login(self):
        """Test to see if user that is not active or not registered
        ca login into the system"""
        user_email = "admin@admin.com"
        user_password = "admin1234"
        res = self.client.post(
            self.login_url,
            {"email_address": user_email, "password": user_password},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestManagerRegisterAdmin(TestSetup):
    """Api test for manager registration of users"""

    def test_manager_register_users(self):
        """Test to see if manager can register a admin user"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.token.access_token)
        )
        response = self.client.post(
            self.admin_register_url,
            data={"email_address": "gyateng@gmail.com", "username": "GyatengER"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_not_managers_can_not_register_admin_users(self):
        """Test to check that managers and only managers can register an admin user"""
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.admin_register_url,
            data={"email_address": "gyatengss@gmail.com", "username": "GyssatengER"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
