from collections import namedtuple

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.constants import Sex
from profiles.models import Location, Profile, UserFromTelegram
from profiles.serializers import ProfileSerializer
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
    LOCATION_M_NAME = "M"
    LOCATION_S_NAME = "S"
    URL_REVERSE = reverse("api-v1:search:profiles")

    @classmethod
    def setUpTestData(cls):
        test_users = [UserFromTelegram.objects.create(
                                        telegram_id=id) for id in range(0, 11)]

        cls.location_m = Location.objects.create(name=cls.LOCATION_M_NAME)
        cls.location_s = Location.objects.create(name=cls.LOCATION_S_NAME)

        ProfileTestData = namedtuple("ProfileTestData",
                                     ["user", "name", "age", "location", "sex"])
        profiles_data = (
            ProfileTestData(test_users[0], "Name_0", 18, cls.location_m, Sex.MAN),
            ProfileTestData(test_users[1], "Name_1", 21, cls.location_m, Sex.MAN),
            ProfileTestData(test_users[2], "Name_2", 25, cls.location_m, Sex.MAN),
            ProfileTestData(test_users[3], "Name_3", 28, cls.location_m, Sex.MAN),
            ProfileTestData(test_users[4], "Name_4", 32, cls.location_m, Sex.WOMAN),
            ProfileTestData(test_users[5], "Name_5", 34, cls.location_m, Sex.WOMAN),
            ProfileTestData(test_users[6], "Name_6", 36, cls.location_s, Sex.MAN),
            ProfileTestData(test_users[7], "Name_7", 38, cls.location_s, Sex.MAN),
            ProfileTestData(test_users[8], "Name_8", 41, cls.location_s, Sex.WOMAN),
            ProfileTestData(test_users[9], "Name_9", 42, cls.location_s, Sex.WOMAN),
            ProfileTestData(test_users[10], "Name_10", 44, cls.location_s, Sex.WOMAN),
            )
        test_profiles = [
            Profile.objects.create(**data._asdict()) for data in profiles_data
            ]

        cls.expected_search_data_1 = {
            "search_criteria":
            {"location": cls.LOCATION_M_NAME, "sex": Sex.MAN,
             "age_min": "20", "age_max": "30"},
            "search_result":
            [ProfileSerializer(test_profiles[2]).data,
             ProfileSerializer(test_profiles[3]).data,]

        }
        cls.expected_search_data_2 = {
            "search_criteria":
            {"location": cls.LOCATION_M_NAME, "sex": Sex.WOMAN,
             "age_min": "30", "age_max": "40"},
            "search_result":
            [ProfileSerializer(test_profiles[4]).data,
             ProfileSerializer(test_profiles[5]).data,]
        }
        cls.expected_search_data_3 = {
            "search_criteria":
            {"location": cls.LOCATION_S_NAME, "sex": Sex.MAN,
             "age_min": "35", "age_max": "40"},
            "search_result":
            [ProfileSerializer(test_profiles[6]).data,
             ProfileSerializer(test_profiles[7]).data,]

        }
        cls.expected_search_data_4 = {
            "search_criteria":
            {"location": cls.LOCATION_S_NAME, "sex": Sex.WOMAN,
             "age_min": "40", "age_max": "50"},
            "search_result":
            [ProfileSerializer(test_profiles[8]).data,
             ProfileSerializer(test_profiles[9]).data,
             ProfileSerializer(test_profiles[10]).data,]
        }

        cls.global_search_results_data = {
            1: cls.expected_search_data_1,
            2: cls.expected_search_data_2,
            3: cls.expected_search_data_3,
            4: cls.expected_search_data_4,
        }

    def test_invalid_methods_match2(self):
        data = {
            "viewer": 1, "location": self.LOCATION_M_NAME,
            "age_min": "25", "age_max": "35", "sex": Sex.MAN
        }
        methods = ["post", "put", "patch", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(method, self.URL_REVERSE, data)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_search_correct_data(self):
        """Тест на корректные результаты поиска для разных критериев."""
        for telegram_id, gsr_data in self.global_search_results_data.items():
            with self.subTest(id=telegram_id, data=gsr_data["search_result"]):
                kwargs = {}
                kwargs["viewer"] = telegram_id
                for key, value in gsr_data["search_criteria"].items():
                    kwargs[key] = value

                response = self.client.get(self.URL_REVERSE, kwargs)
                self.assertEqual(response.json(), gsr_data["search_result"])
