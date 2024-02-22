from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import Location, Profile, UserFromTelegram
from search.constants import MatchStatuses
from search.models import MatchRequest, UserReport


class ReportMatchViewTests(APITestCase):
    """Тесты для UserReportCreateView и MatchedUsersListView."""

    empty_match_data = []

    @classmethod
    def setUpTestData(cls):
        cls.test_user_1 = UserFromTelegram.objects.create(telegram_id=1)
        cls.test_user_2 = UserFromTelegram.objects.create(telegram_id=2)
        cls.test_user_3 = UserFromTelegram.objects.create(telegram_id=3)
        cls.test_user_4 = UserFromTelegram.objects.create(telegram_id=4)
        cls.test_user_5 = UserFromTelegram.objects.create(telegram_id=5)
        cls.location = Location.objects.create(name="location")
        cls.profile_1 = Profile.objects.create(
            user=cls.test_user_1, name="test_1", age=25, location=cls.location
        )
        cls.profile_2 = Profile.objects.create(
            user=cls.test_user_2, name="test_2", age=25, location=cls.location
        )
        cls.profile_3 = Profile.objects.create(
            user=cls.test_user_3, name="test_3", age=25, location=cls.location
        )
        cls.profile_4 = Profile.objects.create(
            user=cls.test_user_4, name="test_4", age=25, location=cls.location
        )
        cls.profile_5 = Profile.objects.create(
            user=cls.test_user_5, name="test_5", age=25, location=cls.location
        )

        cls.match_1 = MatchRequest.objects.create(
            sender=cls.test_user_1,
            receiver=cls.test_user_2,
            status=MatchStatuses.is_match,
        )
        cls.match_3 = MatchRequest.objects.create(
            sender=cls.test_user_3,
            receiver=cls.test_user_1,
            status=MatchStatuses.is_match,
        )
        cls.negative_match = MatchRequest.objects.create(
            sender=cls.test_user_5,
            receiver=cls.test_user_4,
            status=MatchStatuses.is_rejected,
        )

        cls.report_data = {
            "reporter": cls.test_user_1.id,
            "reported_user": cls.test_user_2.id,
            "text": "test_text",
            "category": "Категория 1",
        }

        cls.expected_match_data_for_user_1 = [
            {"telegram_id": 2, "name": "test_2", "age": 25},
            {"telegram_id": 3, "name": "test_3", "age": 25},
        ]

        cls.expected_match_data_for_user_2 = [
            {"telegram_id": 1, "name": "test_1", "age": 25}
        ]

        cls.expected_match_data_for_user_3 = [
            {"telegram_id": 1, "name": "test_1", "age": 25}
        ]

        cls.empty_match_data = []

        cls.global_match_data = {
            1: cls.expected_match_data_for_user_1,
            2: cls.expected_match_data_for_user_2,
            3: cls.expected_match_data_for_user_3,
            4: cls.empty_match_data,
            5: cls.empty_match_data,
        }

    def test_report_create(self):
        """Тест создания жалобы."""
        response = self.client.post(reverse("api-v1:search:report"), self.report_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_in_database(self):
        """Тест наличия жалобы в базе данных после создания."""
        self.client.post(reverse("api-v1:search:report"), self.report_data)
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
        response = self.client.post(reverse("api-v1:search:report"), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data(self):
        """Тест создания жалобы с некорректными данными."""
        invalid_data = {
            "reporter": self.test_user_1.id,
            "reported_user": self.test_user_2.id,
            "text": 999999,
            "category": True,
        }
        response = self.client.post(reverse("api-v1:search:report"), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_required_param_is_absent(self):
        """Тест создания жалобы без обязательных параметров"""
        invalid_data = {
            "reporter": self.test_user_1.id,
            "reported_user": self.test_user_2.id,
        }
        response = self.client.post(reverse("api-v1:search:report"), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_methods_report(self):
        """Тест на незарешенные методы запроса (report)."""
        methods = ["get", "put", "patch", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(method, reverse("api-v1:search:report"))
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_get_match_list(self):
        """Тест получения списка мэтчей."""
        response = self.client.get(
            reverse(
                "api-v1:search:matched-users",
                kwargs={"telegram_id": self.test_user_1.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_match_for_invalid_user(self):
        """Тест получения мэтчей для несуществующего пользователя."""
        response = self.client.get(
            reverse("api-v1:search:matched-users", kwargs={"telegram_id": 99999})
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
                        "api-v1:search:matched-users",
                        kwargs={"telegram_id": self.test_user_1.id},
                    ),
                )
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_matches_correct_data(self):
        """Тест на корректный вывод данных мэтчей."""
        for telegram_id, data in self.global_match_data.items():
            with self.subTest(id=telegram_id, data=data):
                response = self.client.get(
                    reverse(
                        "api-v1:search:matched-users",
                        kwargs={"telegram_id": telegram_id},
                    )
                )
                self.assertEqual(response.json(), data)


class ProfileSearchViewTests(APITestCase):
    """Тесты для ProfilesSearchView."""

    empty_match_data = []

    @classmethod
    def setUpTestData(cls):
        cls.test_user_1 = UserFromTelegram.objects.create(telegram_id=1)
        cls.test_user_2 = UserFromTelegram.objects.create(telegram_id=2)
        cls.test_user_3 = UserFromTelegram.objects.create(telegram_id=3)
        cls.test_user_4 = UserFromTelegram.objects.create(telegram_id=4)
        cls.test_user_5 = UserFromTelegram.objects.create(telegram_id=5)
        cls.test_user_6 = UserFromTelegram.objects.create(telegram_id=6)
        cls.test_user_7 = UserFromTelegram.objects.create(telegram_id=7)
        cls.test_user_8 = UserFromTelegram.objects.create(telegram_id=8)
        cls.test_user_9 = UserFromTelegram.objects.create(telegram_id=9)
        cls.test_user_10 = UserFromTelegram.objects.create(telegram_id=10)
        cls.sex_m = "Парень"
        cls.sex_f = "Девушка"
        cls.location_m = Location.objects.create(name="M")
        cls.location_s = Location.objects.create(name="S")
        cls.profile_1 = Profile.objects.create(
            user=cls.test_user_1, name="Name_1", age=21, location=cls.location_m,
            sex=cls.sex_m
        )
        cls.profile_2 = Profile.objects.create(
            user=cls.test_user_2, name="Name_2", age=25, location=cls.location_m,
            sex=cls.sex_m
        )
        cls.profile_3 = Profile.objects.create(
            user=cls.test_user_3, name="Name_3", age=28, location=cls.location_m,
            sex=cls.sex_m
        )
        cls.profile_4 = Profile.objects.create(
            user=cls.test_user_4, name="Name_4", age=32, location=cls.location_m,
            sex=cls.sex_f
        )
        cls.profile_5 = Profile.objects.create(
            user=cls.test_user_5, name="Name_5", age=34, location=cls.location_m,
            sex=cls.sex_f
        )
        cls.profile_5 = Profile.objects.create(
            user=cls.test_user_6, name="Name_6", age=36, location=cls.location_s,
            sex=cls.sex_m
        )
        cls.profile_5 = Profile.objects.create(
            user=cls.test_user_7, name="Name_7", age=38, location=cls.location_s,
            sex=cls.sex_m
        )
        cls.profile_5 = Profile.objects.create(
            user=cls.test_user_8, name="Name_8", age=41, location=cls.location_s,
            sex=cls.sex_f
        )
        cls.profile_5 = Profile.objects.create(
            user=cls.test_user_9, name="Name_9", age=42, location=cls.location_s,
            sex=cls.sex_f
        )
        cls.profile_5 = Profile.objects.create(
            user=cls.test_user_10, name="Name_10", age=44, location=cls.location_s,
            sex=cls.sex_f
        )

        cls.expected_search_data_1 = {
            "search_criteria":
            {"location": "M", "sex": "Парень", "age_min": "20", "age_max": "30"},
            "search_result":
            [{"telegram_id": 1, "name": "Name_1", "age": 21,
              "location": "M", "sex": cls.sex_m},
             {"telegram_id": 2, "name": "Name_2", "age": 25,
              "location": "M", "sex": cls.sex_m},
             {"telegram_id": 3, "name": "Name_3", "age": 28,
              "location": "M", "sex": cls.sex_m},]
        }
        cls.expected_search_data_2 = {
            "search_criteria":
            {"location": "M", "sex": "Девушка", "age_min": "25", "age_max": "35"},
            "search_result":
            [{"telegram_id": 4, "name": "Name_4", "age": 32,
              "location": "M", "sex": cls.sex_f},
             {"telegram_id": 5, "name": "Name_5", "age": 34,
              "location": "M", "sex": cls.sex_f},]
        }
        cls.expected_search_data_3 = {
            "search_criteria":
            {"location": "S", "sex": "Парень", "age_min": "30", "age_max": "40"},
            "search_result":
            [{"telegram_id": 6, "name": "Name_1", "age": 36,
              "location": "S", "sex": cls.sex_m},
             {"telegram_id": 7, "name": "Name_2", "age": 38,
              "location": "S", "sex": cls.sex_m},]
        }
        cls.expected_search_data_4 = {
            "search_criteria":
            {"location": "S", "sex": "Девушка", "age_min": "35", "age_max": "45"}
            ,
            "search_result":
            [{"telegram_id": 8, "name": "Name_8", "age": 41,
              "location": "S", "sex": cls.sex_f},
             {"telegram_id": 9, "name": "Name_9", "age": 42,
              "location": "S", "sex": cls.sex_f},
             {"telegram_id": 10, "name": "Name_10", "age": 44,
              "location": "S", "sex": cls.sex_f},]
        }

        cls.empty_match_data = []

        cls.global_search_results_data = {
            1: cls.expected_search_data_1,
            2: cls.expected_search_data_2,
            3: cls.expected_search_data_3,
            4: cls.expected_search_data_4,
        }

    def test_invalid_methods_match(self):
        """Тест на некорректные методы запроса (profile-search)."""
        methods = ["post", "put", "patch", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(
                    method,
                    reverse(
                        "api-v1:search:profiles",
                        kwargs={"telegram_id": self.test_user_1.id},
                    ),
                )
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_search_correct_data(self):
        """Тест на корректные результаты поиска для разных критериев."""
        for telegram_id, data in self.global_search_results_data.items():
            with self.subTest(id=telegram_id, data=data["search_result"]):
                kwargs = {}
                kwargs["telegram_id"] = telegram_id
                for key, value in data["search_criteria"]:
                    kwargs[key] += value

                response = self.client.get(
                    reverse(
                        "api-v1:search:profiles",
                        kwargs=kwargs,
                    )
                )
                self.assertEqual(response.json(), data["search_result"])
