from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import Coliving, Location, UserFromTelegram


class ColivingAPITest(APITestCase):
    """Тесты для проверки ресурса Coliving."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFromTelegram.objects.create(telegram_id=1111111)
        cls.user_2 = UserFromTelegram.objects.create(telegram_id=12345678)
        cls.coliving_moscow = Coliving.objects.create(
            host=cls.user,
            price=2500,
            room_type="Комната",
            location=Location.objects.create(name="Москва"),
            about="Уютное пространство...",
        )
        cls.coliving_spb = Coliving.objects.create(
            host=cls.user_2,
            price=2500,
            room_type="Комната",
            location=Location.objects.create(name="Санкт-Петербург"),
            about="Небольшая",
        )


    def test_create_coliving(self):
        """Тест на создание Coliving с валидными данными."""
        url = reverse("api-v1:colivings-list")
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
        url = reverse("api-v1:colivings-list")
        data = {
            "host": 1111111,
            "room_type": "Комната",
            "about": "Уютное пространство...",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_coliving(self):
        """Тест на получение cписка Coliving."""
        url = reverse("api-v1:colivings-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_coliving_id(self):
        """Тест на получение данных Coliving."""
        url = reverse("api-v1:colivings-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_coliving(self):
        """Тест на обновление Coliving с валидными данными."""
        url = reverse("api-v1:colivings-detail", args=[1])
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
        url = reverse("api-v1:colivings-detail", args=[1])
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

    def test_filtres_coliving(self):
        """Тест на филтрацию данных Coliving."""
        response = self.client.get(
            "/api/v1/colivings/",
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

    def test_filtres_owner_coliving(self):
        """Тест на филтрацию данных Coliving."""
        response = self.client.get("/api/v1/colivings/", {"owner": 12345678})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_attach_user_to_coliving(self):
        """Тест на прикрепление пользователя к коливингу."""   # не работает
        url = reverse("api-v1:user-residence-update", kwargs={"telegram_id": self.user.telegram_id})
        data = {"residence": self.coliving_moscow.id}
        response = self.client.patch(url, data, format="json")

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.residence.id, self.coliving_moscow.id)

    def test_detach_user_from_coliving(self):
        """Тест на открепление пользователя от коливинга."""   # не работает
        # Сначала прикрепим пользователя к коливингу
        self.user.residence = self.coliving_moscow
        self.user.save()

        url = reverse("api-v1:user-residence-update", kwargs={"telegram_id": self.user.telegram_id})
        data = {"residence": None}
        response = self.client.patch(url, data, format="json")

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(self.user.residence)

    def test_update_with_invalid_telegram_id(self):
        """Тест обновления с невалидным telegram_id."""
        url = reverse("api-v1:user-residence-update", kwargs={"telegram_id": 999999})  # Несуществующий telegram_id
        data = {"residence": self.coliving_moscow.id}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_with_invalid_residence_id(self):
        """Тест обновления с невалидным residence_id."""
        url = reverse("api-v1:user-residence-update", kwargs={"telegram_id": self.user.telegram_id})
        data = {"residence": 999999}  # Несуществующий ID коливинга
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
