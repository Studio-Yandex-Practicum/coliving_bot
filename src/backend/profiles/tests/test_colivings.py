from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import Coliving, Location, UserFromTelegram

OWNER_1_TELEGRAM_ID = 1111111
OWNER_2_TELEGRAM_ID = 12345678


class ColivingAPITest(APITestCase):
    """Тесты для проверки ресурса Coliving."""

    @classmethod
    def setUpTestData(cls):
        Coliving.objects.create(
            host=UserFromTelegram.objects.create(telegram_id=OWNER_1_TELEGRAM_ID),
            price=2500,
            room_type="Комната",
            location=Location.objects.create(name="Москва"),
            about="Уютное пространство...",
        )
        Coliving.objects.create(
            host=UserFromTelegram.objects.create(telegram_id=OWNER_2_TELEGRAM_ID),
            price=2500,
            room_type="Комната",
            location=Location.objects.create(name="Санкт-Петербург"),
            about="Небольшая",
        )

    def test_create_coliving(self):
        """Тест на создание Coliving с валидными данными."""
        url = reverse("api-v1:profiles:colivings-list")
        data = {
            "host": 1111111,
            "location": "Москва",
            "price": 15000,
            "room_type": "Комната",
            "about": "Уютное пространство...",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_coliving_invalid_data(self):
        """Тест на создание Coliving с невалидными данными."""
        url = reverse("api-v1:profiles:colivings-list")
        data = {
            "host": 1111111,
            "room_type": "Комната",
            "about": "Уютное пространство...",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_coliving(self):
        """Тест на получение cписка Coliving."""
        url = reverse("api-v1:profiles:colivings-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_coliving_id(self):
        """Тест на получение данных Coliving."""
        url = reverse("api-v1:profiles:colivings-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_coliving(self):
        """Тест на обновление Coliving с валидными данными."""
        url = reverse("api-v1:profiles:colivings-detail", args=[1])
        data_list = [
            {"price": 2500},
            {"price": 3500},
        ]

        for data in data_list:
            with self.subTest(data=data):
                response = self.client.patch(
                    url,
                    data,
                    format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_coliving__invalid_data(self):
        """Тест на обновление Coliving с невалидными данными."""
        url = reverse("api-v1:profiles:colivings-detail", args=[1])
        data_list = [
            {"location": "Москва"},
            {"location": "Токио"},
        ]

        for data in data_list:
            with self.subTest(data=data):
                response = self.client.patch(
                    url,
                    data,
                    format="json",
                )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filters_coliving(self):
        """Тест на фильтрацию данных Coliving."""
        response = self.client.get(
            reverse("api-v1:profiles:colivings-list"),
            {
                "location": "Москва",
                "room_type": "Комната",
                "min_price": 2500,
                "max_price ": 3500,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "id": 1,
                    "host": 1111111,
                    "location": "Москва",
                    "price": 2500,
                    "room_type": "Комната",
                    "about": "Уютное пространство...",
                    "is_visible": True,
                    "images": [],
                }
            ],
        )
        self.assertEqual(len(response.data), 1)

    def test_filters_owner_coliving(self):
        """Тест на фильтрацию данных Coliving."""
        response = self.client.get(
            reverse("api-v1:profiles:colivings-list"), {"owner": OWNER_2_TELEGRAM_ID}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
