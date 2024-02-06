from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from profiles.models import Location


class LocationListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Location.objects.create(name="Location 1")
        Location.objects.create(name="Location 2")

    def test_location_list_status_code(self):
        url = reverse("api-v1:locations-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_list_response_data(self):
        url = reverse("api-v1:locations-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [{"id": 1, "name": "Location 1"}, {"id": 2, "name": "Location 2"}],
        )

    def test_location_list_idempotent(self):
        url = reverse("api-v1:locations-list")
        response1 = self.client.get(url)
        response2 = self.client.get(url)
        self.assertEqual(response1.data, response2.data)
