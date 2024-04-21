from collections import namedtuple

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.constants import Sex
from profiles.models import Location, Profile, UserFromTelegram
from profiles.serializers import ProfileSerializer
from search.models import UserReport


class ReportViewTests(APITestCase):
    """Тесты для UserReportCreateView и MatchedUsersListView."""

    URL_REVERSE = reverse("api-v1:search:report")
    AGE_25 = 25
    REPORT_TEXT = "test_text"
    CATEGORY_TEXT = "Категория 1"
    TELEGRAM_ID_TXT = "telegram_id"
    AGE_TXT = "age"
    LOCATION_TXT = "location"
    NAME_TXT = "name"

    @classmethod
    def setUpTestData(cls):
        cls.t_users = [
            UserFromTelegram.objects.create(telegram_id=id) for id in range(1, 6)
        ]
        cls.t_names = [f"test_{x}" for x in range(1, 6)]
        cls.location = Location.objects.create(name=cls.LOCATION_TXT)
        ProfileTestData = namedtuple(
            "ProfileTestData", ["user", cls.NAME_TXT, cls.AGE_TXT, cls.LOCATION_TXT]
        )

        profiles_data = (
            ProfileTestData(cls.t_users[0], cls.t_names[0], cls.AGE_25, cls.location),
            ProfileTestData(cls.t_users[1], cls.t_names[1], cls.AGE_25, cls.location),
            ProfileTestData(cls.t_users[2], cls.t_names[2], cls.AGE_25, cls.location),
            ProfileTestData(cls.t_users[3], cls.t_names[3], cls.AGE_25, cls.location),
            ProfileTestData(cls.t_users[4], cls.t_names[4], cls.AGE_25, cls.location),
        )
        [Profile.objects.create(**data._asdict()) for data in profiles_data]

        cls.report_data = {
            "reporter": cls.t_users[0].pk,
            "reported_user": cls.t_users[1].pk,
            "text": cls.REPORT_TEXT,
            "category": cls.CATEGORY_TEXT,
        }

        cls.expected_match_data_for_user_1 = [
            {
                cls.TELEGRAM_ID_TXT: 2,
                cls.NAME_TXT: cls.t_names[1],
                cls.AGE_TXT: cls.AGE_25,
            },
            {
                cls.TELEGRAM_ID_TXT: 3,
                cls.NAME_TXT: cls.t_names[2],
                cls.AGE_TXT: cls.AGE_25,
            },
        ]

        cls.expected_match_data_for_user_2 = [
            {
                cls.TELEGRAM_ID_TXT: 1,
                cls.NAME_TXT: cls.t_names[0],
                cls.AGE_TXT: cls.AGE_25,
            }
        ]

        cls.expected_match_data_for_user_3 = [
            {
                cls.TELEGRAM_ID_TXT: 1,
                cls.NAME_TXT: cls.t_names[0],
                cls.AGE_TXT: cls.AGE_25,
            }
        ]

        cls.global_match_data = {
            1: cls.expected_match_data_for_user_1,
            2: cls.expected_match_data_for_user_2,
            3: cls.expected_match_data_for_user_3,
            4: [],
            5: [],
        }

    def test_report_create(self):
        """Тест создания жалобы."""
        response = self.client.post(self.URL_REVERSE, self.report_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_in_database(self):
        """Тест наличия жалобы в базе данных после создания."""
        self.client.post(self.URL_REVERSE, self.report_data)
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
            "reporter": self.t_users[0].pk,
            "reported_user": 99999,
            "text": "test_text_2",
            "category": "Категория 2",
        }
        response = self.client.post(self.URL_REVERSE, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data(self):
        """Тест создания жалобы с некорректными данными."""
        invalid_data = {
            "reporter": self.t_users[0].pk,
            "reported_user": self.t_users[1].pk,
            "text": 999999,
            "category": True,
        }
        response = self.client.post(self.URL_REVERSE, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_required_param_is_absent(self):
        """Тест создания жалобы без обязательных параметров"""
        invalid_data = {
            "reporter": self.t_users[0].pk,
            "reported_user": self.t_users[1].pk,
        }
        response = self.client.post(self.URL_REVERSE, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_methods_report(self):
        """Тест на незарешенные методы запроса (report)."""
        methods = ["get", "put", "patch", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(method, self.URL_REVERSE)
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )


class ProfileSearchViewTests(APITestCase):
    """Тесты для ProfilesSearchView."""

    LOCATION_M_NAME = "M"
    LOCATION_S_NAME = "S"
    URL_REVERSE = reverse("api-v1:search:profiles")

    @classmethod
    def setUpTestData(cls):
        test_users = [
            UserFromTelegram.objects.create(telegram_id=id) for id in range(0, 11)
        ]
        p_names = [f"Name_{x}" for x in range(0, 11)]

        cls.location_m = Location.objects.create(name=cls.LOCATION_M_NAME)
        cls.location_s = Location.objects.create(name=cls.LOCATION_S_NAME)

        ProfileTestData = namedtuple(
            "ProfileTestData", ["user", "name", "age", "location", "sex"]
        )
        profiles_data = (
            ProfileTestData(test_users[0], p_names[0], 18, cls.location_m, Sex.MAN),
            ProfileTestData(test_users[1], p_names[1], 21, cls.location_m, Sex.MAN),
            ProfileTestData(test_users[2], p_names[2], 25, cls.location_m, Sex.MAN),
            ProfileTestData(test_users[3], p_names[3], 28, cls.location_m, Sex.MAN),
            ProfileTestData(test_users[4], p_names[4], 32, cls.location_m, Sex.WOMAN),
            ProfileTestData(test_users[5], p_names[5], 34, cls.location_m, Sex.WOMAN),
            ProfileTestData(test_users[6], p_names[6], 36, cls.location_s, Sex.MAN),
            ProfileTestData(test_users[7], p_names[7], 38, cls.location_s, Sex.MAN),
            ProfileTestData(test_users[8], p_names[8], 41, cls.location_s, Sex.WOMAN),
            ProfileTestData(test_users[9], p_names[9], 42, cls.location_s, Sex.WOMAN),
            ProfileTestData(test_users[10], p_names[10], 44, cls.location_s, Sex.WOMAN),
        )
        test_profiles = [
            Profile.objects.create(**data._asdict()) for data in profiles_data
        ]

        cls.expected_search_data_1 = {
            "search_criteria": {
                "location": cls.LOCATION_M_NAME,
                "sex": Sex.MAN,
                "age_min": "20",
                "age_max": "30",
            },
            "search_result": [
                ProfileSerializer(test_profiles[2]).data,
                ProfileSerializer(test_profiles[3]).data,
            ],
        }
        cls.expected_search_data_2 = {
            "search_criteria": {
                "location": cls.LOCATION_M_NAME,
                "sex": Sex.WOMAN,
                "age_min": "30",
                "age_max": "40",
            },
            "search_result": [
                ProfileSerializer(test_profiles[4]).data,
                ProfileSerializer(test_profiles[5]).data,
            ],
        }
        cls.expected_search_data_3 = {
            "search_criteria": {
                "location": cls.LOCATION_S_NAME,
                "sex": Sex.MAN,
                "age_min": "35",
                "age_max": "40",
            },
            "search_result": [
                ProfileSerializer(test_profiles[6]).data,
                ProfileSerializer(test_profiles[7]).data,
            ],
        }
        cls.expected_search_data_4 = {
            "search_criteria": {
                "location": cls.LOCATION_S_NAME,
                "sex": Sex.WOMAN,
                "age_min": "40",
                "age_max": "50",
            },
            "search_result": [
                ProfileSerializer(test_profiles[8]).data,
                ProfileSerializer(test_profiles[9]).data,
                ProfileSerializer(test_profiles[10]).data,
            ],
        }

        cls.global_search_results_data = {
            1: cls.expected_search_data_1,
            2: cls.expected_search_data_2,
            3: cls.expected_search_data_3,
            4: cls.expected_search_data_4,
        }

    def test_invalid_methods_match2(self):
        data = {
            "viewer": 1,
            "location": self.LOCATION_M_NAME,
            "age_min": "25",
            "age_max": "35",
            "sex": Sex.MAN,
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
            with self.subTest(viewer=telegram_id, data=gsr_data["search_result"]):
                kwargs = {}
                kwargs["viewer"] = telegram_id
                for key, value in gsr_data["search_criteria"].items():
                    kwargs[key] = value

                response = self.client.get(self.URL_REVERSE, kwargs)
                self.assertEqual(response.json(), gsr_data["search_result"])
