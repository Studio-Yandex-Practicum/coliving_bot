from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Location
import json


class LocationListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Location.objects.create(name='Location 1')
        Location.objects.create(name='Location 2')

    def test_location_list_status_code(self):
        response = self.client.get('/api/v1/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_list_response_data(self):
        response = self.client.get('/api/v1/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'id')
        self.assertContains(response, 'name')
        self.assertContains(response, 'Location 1')
        self.assertContains(response, 'Location 2')

    def test_location_list_idempotent(self):
        response1 = self.client.get('/api/v1/locations/')
        response2 = self.client.get('/api/v1/locations/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        data1 = json.loads(response1.content.decode('utf-8'))
        data2 = json.loads(response2.content.decode('utf-8'))
        self.assertEqual(data1, data2)
