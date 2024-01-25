from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import Location, Profile, UserFromTelegram

TEST_TELEGRAM_ID = 12345
EXISTING_PROFILE_TELEGRAM_ID = 877877
NON_EXISTENT_PROFILE_TELEGRAM_ID = 99999


class ProfileAPITestCase(APITestCase):
    """Тесты для проверки ресурса Profile."""

    @classmethod
    def setUpTestData(cls):
        cls.fields_to_check = ["name", "sex", "age", "about", "is_visible"]
        cls.profile_1 = Profile.objects.create(
            user=UserFromTelegram.objects.create(
                telegram_id=EXISTING_PROFILE_TELEGRAM_ID
            ),
            name="test_1",
            sex="Парень",
            age=25,
            location=Location.objects.create(name="Санкт-Петербург"),
            about="Классный",
        )
        UserFromTelegram.objects.create(telegram_id=TEST_TELEGRAM_ID)

    def test_create_profile(self):
        """Тест на создание профиля с валидными данными."""
        data = {
            "name": "Иван",
            "sex": "Парень",
            "age": 22,
            "location": "Санкт-Петербург",
            "about": "Классный",
        }
        response = self.client.post(
            reverse("api-v1:user-profile", args=[TEST_TELEGRAM_ID]), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_profile_data(response, TEST_TELEGRAM_ID, data)

    def test_create_profile_invalid_data(self):
        """Тест на создание профиля с невалидными данными."""
        data = {"name": "Иван", "sex": "Парень", "age": 22, "about": "Классный"}
        response = self.client.post(
            reverse("api-v1:user-profile", args=[TEST_TELEGRAM_ID]), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            Profile.objects.filter(user__telegram_id=TEST_TELEGRAM_ID).count(), 0
        )

    def test_get_existing_profile(self):
        """Тест на получение данных профиля."""
        response = self.client.get(
            reverse("api-v1:user-profile", args=[EXISTING_PROFILE_TELEGRAM_ID])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_profile_data(response, EXISTING_PROFILE_TELEGRAM_ID)

    def test_get_nonexistent_profile(self):
        """Тест на получение данных несуществующего профиля."""
        response = self.client.get(
            reverse("api-v1:user-profile", args=[NON_EXISTENT_PROFILE_TELEGRAM_ID])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": "Not found."})
        self.assertEqual(
            Profile.objects.filter(
                user__telegram_id=NON_EXISTENT_PROFILE_TELEGRAM_ID
            ).count(),
            0,
        )

    def test_patch_profile_update_fields(self):
        """Тест на обновление профиля с валидными данными."""
        data_list = [
            {"name": "Иван Иванов", "about": "Очень классный", "is_visible": True},
            {"name": "Кирилл", "age": 23, "location": "Санкт-Петербург"},
        ]

        for data in data_list:
            with self.subTest(data=data):
                response = self.client.patch(
                    reverse("api-v1:user-profile", args=[EXISTING_PROFILE_TELEGRAM_ID]),
                    data,
                    format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assert_profile_data(response, EXISTING_PROFILE_TELEGRAM_ID)

    def test_patch_profile_invalid_data(self):
        """Тест на обновление профиля с невалидными данными."""
        data = {"name": "Кирилл", "age": 23, "location": "Екатеринбург"}
        response = self.client.patch(
            reverse("api-v1:user-profile", args=[EXISTING_PROFILE_TELEGRAM_ID]),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"location": ["Object with name=Екатеринбург does not exist."]},
        )

    def assert_profile_data(self, response, telegram_id, data=None):
        """Проверка содержимого полей ответа."""
        profile = Profile.objects.get(user__telegram_id=telegram_id)
        self.assertEqual(
            Profile.objects.filter(user__telegram_id=telegram_id).count(), 1
        )
        if data:
            for field in self.fields_to_check:
                self.assertEqual(response.data[field], getattr(profile, field))
            self.assertEqual(response.data["location"], data["location"])
        self.assertEqual(response.data["user"], telegram_id)

    def test_invalid_methods_profile(self):
        """Тест на незарешенные методы запроса."""
        methods = ["put", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(
                    method,
                    reverse("api-v1:user-profile", args=[EXISTING_PROFILE_TELEGRAM_ID]),
                )
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )
