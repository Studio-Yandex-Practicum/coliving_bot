from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from profiles.models import Location, Profile, UserFromTelegram

TEST_TELEGRAM_ID = 12345
EXISTING_PROFILE_TELEGRAM_ID = 877877
NON_EXISTENT_PROFILE_TELEGRAM_ID = 99999


class ProfileAPITestCase(APITestCase):
    """Тесты для проверки ресурса Profile."""

    VIEW_LINK = "api-v1:profiles:user-profile"
    AGE_22 = 22
    AGE_23 = 23
    LOC_SPB_TXT = "Санкт-Петербург"
    NAME_KIRILL = "Кирилл"
    NAME_IVAN = "Иван"
    NAME_TXT = "name"
    SEX_TXT = "sex"
    AGE_TXT = "age"
    LOCATION_TXT = "location"
    ABOUT_TXT = "about"
    VISIBLE_TXT = "is_visible"
    PAREN_TXT = "Парень"
    KLASSNIY_TXT = "Классный"
    JSON_TXT = "json"

    @classmethod
    def setUpTestData(cls):
        cls.fields_to_check = [
            cls.NAME_TXT,
            cls.SEX_TXT,
            cls.AGE_TXT,
            cls.ABOUT_TXT,
            cls.VISIBLE_TXT,
        ]
        cls.profile_1 = Profile.objects.create(
            user=UserFromTelegram.objects.create(
                telegram_id=EXISTING_PROFILE_TELEGRAM_ID
            ),
            name="test_1",
            sex=cls.PAREN_TXT,
            age=25,
            location=Location.objects.create(name=cls.LOC_SPB_TXT),
            about=cls.KLASSNIY_TXT,
        )
        UserFromTelegram.objects.create(telegram_id=TEST_TELEGRAM_ID)

    def test_create_profile(self):
        """Тест на создание профиля с валидными данными."""
        data = {
            self.NAME_TXT: self.NAME_IVAN,
            self.SEX_TXT: self.PAREN_TXT,
            self.AGE_TXT: self.AGE_22,
            self.LOCATION_TXT: self.LOC_SPB_TXT,
            self.ABOUT_TXT: self.KLASSNIY_TXT,
        }
        response = self.client.post(
            reverse(self.VIEW_LINK, args=[TEST_TELEGRAM_ID]),
            data,
            format=self.JSON_TXT,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_profile_data(response, TEST_TELEGRAM_ID, data)

    def test_create_profile_invalid_data(self):
        """Тест на создание профиля с невалидными данными."""
        data = {
            self.NAME_TXT: self.NAME_IVAN,
            self.SEX_TXT: self.PAREN_TXT,
            self.AGE_TXT: self.AGE_22,
            self.ABOUT_TXT: self.KLASSNIY_TXT,
        }
        response = self.client.post(
            reverse(self.VIEW_LINK, args=[TEST_TELEGRAM_ID]),
            data,
            format=self.JSON_TXT,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            Profile.objects.filter(user__telegram_id=TEST_TELEGRAM_ID).exists()
        )

    def test_get_existing_profile(self):
        """Тест на получение данных профиля."""
        response = self.client.get(
            reverse(self.VIEW_LINK, args=[EXISTING_PROFILE_TELEGRAM_ID])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_profile_data(response, EXISTING_PROFILE_TELEGRAM_ID)

    def test_get_nonexistent_profile(self):
        """Тест на получение данных несуществующего профиля."""
        response = self.client.get(
            reverse(self.VIEW_LINK, args=[NON_EXISTENT_PROFILE_TELEGRAM_ID])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(
            Profile.objects.filter(
                user__telegram_id=NON_EXISTENT_PROFILE_TELEGRAM_ID
            ).exists(),
        )

    def test_patch_profile_update_fields(self):
        """Тест на обновление профиля с валидными данными."""
        data_list = [
            {
                self.NAME_TXT: "Иван Иванов",
                self.ABOUT_TXT: "Очень классный",
                self.VISIBLE_TXT: True,
            },
            {
                self.NAME_TXT: self.NAME_KIRILL,
                self.AGE_TXT: self.AGE_23,
                self.LOCATION_TXT: self.LOC_SPB_TXT,
            },
        ]

        for data in data_list:
            with self.subTest(data=data):
                response = self.client.patch(
                    reverse(
                        self.VIEW_LINK,
                        args=[EXISTING_PROFILE_TELEGRAM_ID],
                    ),
                    data,
                    format=self.JSON_TXT,
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assert_profile_data(response, EXISTING_PROFILE_TELEGRAM_ID)

    def test_patch_profile_invalid_data(self):
        """Тест на обновление профиля с невалидными данными."""
        data = {
            self.NAME_TXT: self.NAME_KIRILL,
            self.AGE_TXT: self.AGE_23,
            self.LOCATION_TXT: "Екатеринбург",
        }
        response = self.client.patch(
            reverse(self.VIEW_LINK, args=[EXISTING_PROFILE_TELEGRAM_ID]),
            data,
            format=self.JSON_TXT,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data[self.LOCATION_TXT][0], ErrorDetail)

    def assert_profile_data(self, response, telegram_id, data=None):
        """Проверка содержимого полей ответа."""
        profile = Profile.objects.get(user__telegram_id=telegram_id)
        self.assertEqual(
            Profile.objects.filter(user__telegram_id=telegram_id).count(), 1
        )
        if data:
            for field in self.fields_to_check:
                self.assertEqual(response.data[field], getattr(profile, field))
            self.assertEqual(response.data[self.LOCATION_TXT], data[self.LOCATION_TXT])
        self.assertEqual(response.data["user"], telegram_id)

    def test_invalid_methods_profile(self):
        """Тест на незарешенные методы запроса."""
        methods = ["put", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(
                    method,
                    reverse(
                        self.VIEW_LINK,
                        args=[EXISTING_PROFILE_TELEGRAM_ID],
                    ),
                )
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )
