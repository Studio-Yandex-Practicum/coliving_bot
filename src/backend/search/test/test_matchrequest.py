from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from search.constants import MatchStatuses
from profiles.models import  UserFromTelegram
from search.models import MatchRequest

class MatchRequestAPITest(APITestCase):
    """Тесты для проверки ресурса MatchRequest."""
    def setUp(cls):
        MatchRequest.objects.create(
            sender=UserFromTelegram.objects.create(telegram_id=1234567),
            receiver=UserFromTelegram.objects.create(telegram_id=1234568),
            status=MatchStatuses.is_pending,)
    
        UserFromTelegram.objects.create(telegram_id=234569)
        UserFromTelegram.objects.create(telegram_id=234567)
    def test_create_MatchRequest(self):
        """Тест на создание  нового MatchRequest."""
        url = reverse('api-v1:match-request')
        data = {"sender": 234569,
                "receiver": 234567, }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_MatchRequest(self):
        """Тест на совподение MatchRequest."""
        url = reverse('api-v1:match-request')
        data = {"sender": 1234568,
                "receiver": 1234567, }
        response = self.client.post(url, data, format="json")
        updated_object = MatchRequest.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(updated_object.status, MatchStatuses.is_match)