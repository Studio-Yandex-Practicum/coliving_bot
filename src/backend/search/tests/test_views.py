from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import Location, Profile, UserFromTelegram
from search.constants import MatchStatuses
from search.models import MatchRequest, UserReport


class ReportMatchViewTests(APITestCase):
    """Тесты для UserReportCreateView и MatchedUsersListView."""

    def setUp(self):
        self.test_user_1 = UserFromTelegram.objects.create(telegram_id=1)
        self.test_user_2 = UserFromTelegram.objects.create(telegram_id=2)
        self.test_user_3 = UserFromTelegram.objects.create(telegram_id=3)
        self.test_user_4 = UserFromTelegram.objects.create(telegram_id=4)
        self.test_user_5 = UserFromTelegram.objects.create(telegram_id=5)
        self.location = Location.objects.create(name="location")
        self.profile_1 = Profile.objects.create(
            user=self.test_user_1, name="test_1", age=25, location=self.location
        )
        self.profile_2 = Profile.objects.create(
            user=self.test_user_2, name="test_2", age=25, location=self.location
        )
        self.profile_3 = Profile.objects.create(
            user=self.test_user_3, name="test_3", age=25, location=self.location
        )
        self.profile_4 = Profile.objects.create(
            user=self.test_user_4, name="test_4", age=25, location=self.location
        )
        self.profile_5 = Profile.objects.create(
            user=self.test_user_5, name="test_5", age=25, location=self.location
        )

        self.match_1 = MatchRequest.objects.create(
            sender=self.test_user_1,
            receiver=self.test_user_2,
            status=MatchStatuses.is_match,
        )
        self.match_2 = MatchRequest.objects.create(
            sender=self.test_user_2,
            receiver=self.test_user_1,
            status=MatchStatuses.is_match,
        )
        self.match_3 = MatchRequest.objects.create(
            sender=self.test_user_3,
            receiver=self.test_user_1,
            status=MatchStatuses.is_match,
        )
        self.negative_match = MatchRequest.objects.create(
            sender=self.test_user_5,
            receiver=self.test_user_1,
            status=MatchStatuses.is_rejected,
        )

        self.report_data = {
            "reporter": self.test_user_1.id,
            "reported_user": self.test_user_2.id,
            "text": "test_text",
            "category": "Категория 1",
        }

        self.expected_match_data_for_user_1 = [
            {"telegram_id": 2, "name": "test_2", "age": 25},
            {"telegram_id": 3, "name": "test_3", "age": 25},
        ]

        self.expected_match_data_for_user_2 = [
            {"telegram_id": 1, "name": "test_1", "age": 25}
        ]

        self.empty_match_data = []

        self.global_match_data = {
            1: self.expected_match_data_for_user_1,
            2: self.expected_match_data_for_user_2,
            4: self.empty_match_data,
            5: self.empty_match_data,
        }

    def test_report_create(self):
        """Тест создания жалобы."""
        response = self.client.post(reverse("report"), self.report_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_in_database(self):
        """Тест наличия жалобы в базе данных после создания."""
        self.client.post(reverse("report"), self.report_data, format="json")
        created_report = UserReport.objects.filter(
            reporter=self.report_data["reporter"],
            reported_user=self.report_data["reported_user"],
            text=self.report_data["text"],
            category=self.report_data["category"],
        ).first()
        self.assertIsNotNone(created_report)

    def test_invalid_reported_user(self):
        """Тест создания жалобы на несуществующиего пользователя."""
        invalid_data = {
            "reporter": self.test_user_1.id,
            "reported_user": 99999,
            "text": "test_text_2",
            "category": "Категория 2",
        }
        response = self.client.post(reverse("report"), invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data(self):
        """Тест создания жалобы с некорректными данными."""
        invalid_data = {
            "reporter": self.test_user_1.id,
            "reported_user": self.test_user_2.id,
            "text": 999999,
            "category": True,
        }
        response = self.client.post(reverse("report"), invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_required_param_is_absent(self):
        """Тест создания жалобы без обязательных параметров"""
        invalid_data = {
            "reporter": self.test_user_1.id,
            "reported_user": self.test_user_2.id,
        }
        response = self.client.post(reverse("report"), invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_methods_report(self):
        """Тест на незарешенные методы запроса (report)."""
        methods = ["get", "put", "patch", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(method, reverse("report"))
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_get_match_list(self):
        """Тест получения списка мэтчей."""
        response = self.client.get(
            reverse("matched-users", kwargs={"telegram_id": self.test_user_1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_match_for_invalid_user(self):
        """Тест получения мэтчей для несуществующего пользователя."""
        response = self.client.get(
            reverse("matched-users", kwargs={"telegram_id": 99999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_methods_match(self):
        """Тест на незарешенные методы запроса (match)."""
        methods = ["post", "put", "patch", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(
                    method,
                    reverse(
                        "matched-users", kwargs={"telegram_id": self.test_user_1.id}
                    ),
                )
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_matches_correct_data(self):
        """Тест на корректный вывод данных мэтчей."""
        for id, data in self.global_match_data.items():
            with self.subTest(id=id, data=data):
                response = self.client.get(
                    reverse("matched-users", kwargs={"telegram_id": id})
                )
                self.assertEqual(response.json(), data)
