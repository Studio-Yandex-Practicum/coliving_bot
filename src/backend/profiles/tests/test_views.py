from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.constants import ColivingTypes
from profiles.models import Coliving, Location, UserFromTelegram


class UpdateUserLocationTests(APITestCase):
    """Тесты для UpdateUserLocationView."""

    @classmethod
    def setUpTestData(cls):
        cls.test_user_1 = UserFromTelegram.objects.create(telegram_id=1)
        cls.location_1 = Location.objects.create(name="Москва")
        cls.location_2 = Location.objects.create(name="Санкт-Петербург")
        cls.coliving_1 = Coliving.objects.create(
            host=cls.test_user_1,
            price=100,
            room_type=ColivingTypes.ROOM,
            location=cls.location_1,
        )
        cls.coliving_2 = Coliving.objects.create(
            host=cls.test_user_1,
            price=200,
            room_type=ColivingTypes.PLACE,
            location=cls.location_2,
        )
        cls.test_user_2 = UserFromTelegram.objects.create(
            telegram_id=2, residence=cls.coliving_1
        )

        cls.coliving_data = {"residence": 2}
        cls.invalid_data = {"residence": 99999}

    def test_change_coliving(self):
        """Тест смены коливинга."""
        response = self.client.patch(
            reverse(
                "update-user-location", kwargs={"telegram_id": self.test_user_2.id}
            ),
            self.coliving_data,
        )
        changed_user = UserFromTelegram.objects.filter(
            residence=self.coliving_data["residence"]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(changed_user)

    def test_invalid_change_coliving(self):
        """Тест изменения коливинга на несуществующий."""
        response = self.client.patch(
            reverse(
                "update-user-location", kwargs={"telegram_id": self.test_user_2.id}
            ),
            self.invalid_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_methods_report(self):
        """Тест на незарешенные методы запроса (report)."""
        methods = ["get", "post", "delete"]
        for method in methods:
            with self.subTest(method=method):
                response = self.client.generic(
                    method,
                    reverse(
                        "update-user-location",
                        kwargs={"telegram_id": self.test_user_2.id},
                    ),
                    self.coliving_data,
                )
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )
