from rest_framework.test import APITestCase

from profiles.constants import ColivingTypes
from profiles.models import Coliving, Location, UserFromTelegram
from profiles.serializers import UserSerializer


class UserSerializerTests(APITestCase):
    """Тесты для UserSerializer."""

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

        cls.invalid_data = {"residence": "wrong_type"}
        cls.data = {
            "residence": 2,
        }

    def test_invalid_data(self):
        """Тест на сериализацию некорректных данных."""
        serializer = UserSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_missing_required_field(self):
        """Тест на сериализацию пустых данных."""
        invalid_data = {}
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_valid_data_change_coliving(self):
        """Тест смены коливинга с валидными данными."""
        serializer = UserSerializer(instance=self.test_user_2, data=self.data)
        serializer.is_valid()
        serializer.save()
        changed_user = UserFromTelegram.objects.get(residence=self.coliving_2)
        self.assertIsNotNone(changed_user)
        self.assertEqual(changed_user.residence, self.coliving_2)
