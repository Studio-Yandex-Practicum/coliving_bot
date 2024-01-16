from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import UserFromTelegram

# from search.models import UserReport, MatchRequest


class ReportTests(APITestCase):
    """Тесты для UserReportCreateView."""

    def setUP(self):
        self.test_user_1 = UserFromTelegram.objects.create(id=1)
        self.test_user_1.save()
        self.test_user_2 = UserFromTelegram.objects.create(id=2)
        self.test_user_2.save()

        self.data = {
            "reporter": self.test_user_1,
            "reported_user": self.test_user_2,
            "text": "test_text",
            "category": "Категория 1",
        }

    def test_report_create(self):
        """Тест создания жалобы."""
        response = self.client.post(reverse("report", self.data, format="json"))
        print("fdsfsdfsdf")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
