"""Test cases for Flights application"""
import pdb
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from authentications.models import Users
from flights.models import Flights

# Create your tests here.
class TestSetup(APITestCase):
    """Setup class for the test cases"""

    def setUp(self):
        """Setup of the test"""
        self.admin_url = "/flight/admin/create/"
        self.manager_url = "/flight/manager/update/5/"
        self.superuser = Users.objects.create_superuser(
            username="manager", email_address="manager@admin.com", password="admin1234"
        )
        self.admin_user = Users.objects.create_admin(
            first_name="New",
            last_name="Trial",
            username="admin",
            email_address="admin@admin.com",
            password="admin1234",
        )
        self.flight_data = {
            "flight_name": "Ceasar",
            "source": "Ghana",
            "destination": "Egland",
            "price_per_seat": 300,
            "seats_available": 40,
            "plane_name": "AWA",
            "time_of_departure": "2022-10-06T12:45:00Z",
            "time_of_arrival": "2022-10-06T16:45:00Z",
        }
        self.create_flight = Flights.objects.create(
            flight_name="Ceasar",
            source="Ghana",
            destination="Egland",
            price_per_seat=300,
            seats_available=40,
            plane_name="AWA",
            time_of_departure="2022-10-06T12:45:00Z",
            time_of_arrival="2022-10-06T16:45:00Z",
        )
        self.create_flight.save()
        self.flight_update_data = {"is_approved": True}
        self.admin_token = RefreshToken.for_user(self.admin_user)
        self.superuser_token = RefreshToken.for_user(self.superuser)
        return super().setUp()


class AdminCreateFlights(TestSetup):
    """Test admin can create flight"""

    def test_admin_create_flight(self):
        """Admin creating flight test case"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.admin_token.access_token)
        )
        response = self.client.post(
            self.admin_url,
            self.flight_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_managers_can_create_flight(self):
        """Manager creating flight test case"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.superuser_token.access_token)
        )
        response = self.client.post(
            self.admin_url,
            self.flight_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestManagersUpdateFlight(TestSetup):
    """Testing manager updating flights"""

    def test_managers_can_approve_flight(self):
        """Managers approving flight test case"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.superuser_token.access_token)
        )
        response = self.client.patch(
            self.manager_url,
            self.flight_update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_managers_can_delete_flight(self):
        """Admin deleting flight test case"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.superuser_token.access_token)
        )
        response = self.client.delete(self.manager_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
