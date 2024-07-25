from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.constants import Restrictions, Sex
from profiles.models import Coliving, ColivingTypes, Location, Profile, UserFromTelegram
from search.models import ColivingLike

TELEGR_ID_TXT = "telegram_id"
LOCATION_TXT = "location"
ROOM_TYPE_TXT = "room_type"
PRC_TXT = "price"
MAX_PRC_TXT = "max_price"
MIN_PRC_TXT = "min_price"
VIEWER_TXT = "viewer"
RESIDENCE_TXT = "residence"
HOST_TXT = "host"
ABOUT_TXT = "about"
IS_VISIBLE_TXT = "is_visible"
SOME_TXT = "Some text"
ID_TXT = "id"

VIEW_USER_DET_LINK = "api-v1:profiles:users-detail"
VIEW_COL_LIST_LINK = "api-v1:profiles:colivings-list"
VIEW_COL_DET_LINK = "api-v1:profiles:colivings-detail"
VIEW_COL_RET_LINK = "api-v1:profiles:coliving-residence"


class ColivingAPITest(APITestCase):
    """Тесты для проверки ресурса Coliving."""

    OWNER_1_TELEGRAM_ID = 111
    MSK_LOCATION_NAME = "Москва"
    OWNER_1_ABOUT = "Уютное пространство..."

    OWNER_2_TELEGRAM_ID = 222
    SPB_LOCATION_NAME = "Санкт-Петербург"

    UNKNOWN_LOCATION = "UNKNOWN_LOCATION"

    @classmethod
    def setUpTestData(cls):
        Coliving.objects.create(
            host=UserFromTelegram.objects.create(telegram_id=cls.OWNER_1_TELEGRAM_ID),
            price=Restrictions.PRICE_MIN,
            room_type=ColivingTypes.ROOM,
            location=Location.objects.create(name=cls.MSK_LOCATION_NAME),
            about=cls.OWNER_1_ABOUT,
        )

        spb_location = Location.objects.create(name=cls.SPB_LOCATION_NAME)
        owner_2 = UserFromTelegram.objects.create(telegram_id=cls.OWNER_2_TELEGRAM_ID)
        Coliving.objects.create(
            host=owner_2,
            price=Restrictions.PRICE_MIN,
            room_type=ColivingTypes.ROOM,
            location=spb_location,
            is_visible=True,
        )
        Coliving.objects.create(
            host=owner_2,
            price=Restrictions.PRICE_MIN,
            room_type=ColivingTypes.ROOM,
            location=spb_location,
            is_visible=False,
        )

    def test_create_coliving(self):
        """Тест на создание Coliving с валидными данными."""
        url = reverse(VIEW_COL_LIST_LINK)
        data = {
            HOST_TXT: self.OWNER_1_TELEGRAM_ID,
            LOCATION_TXT: self.MSK_LOCATION_NAME,
            PRC_TXT: Restrictions.PRICE_MAX,
            ROOM_TYPE_TXT: ColivingTypes.ROOM,
            ABOUT_TXT: SOME_TXT,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_coliving_invalid_data(self):
        """Тест на создание Coliving с невалидными данными."""
        url = reverse(VIEW_COL_LIST_LINK)
        data = {
            HOST_TXT: self.OWNER_1_TELEGRAM_ID,
            ROOM_TYPE_TXT: ColivingTypes.ROOM,
            ABOUT_TXT: SOME_TXT,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_coliving(self):
        """Тест на получение cписка Coliving."""
        url = reverse(VIEW_COL_LIST_LINK)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_coliving_id(self):
        """Тест на получение данных Coliving."""
        url = reverse(VIEW_COL_DET_LINK, args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_coliving(self):
        """Тест на обновление Coliving с валидными данными."""
        url = reverse(VIEW_COL_DET_LINK, args=[1])
        data_list = [
            {PRC_TXT: Restrictions.PRICE_MIN},
            {PRC_TXT: Restrictions.PRICE_MAX},
        ]

        for data in data_list:
            with self.subTest(data=data):
                response = self.client.patch(
                    url,
                    data,
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_coliving__invalid_data(self):
        """Тест на обновление Coliving с невалидными данными."""
        url = reverse(VIEW_COL_DET_LINK, args=[1])
        data = {LOCATION_TXT: self.UNKNOWN_LOCATION}
        response = self.client.patch(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filters_coliving(self):
        """Тест на фильтрацию данных Coliving."""
        response = self.client.get(
            reverse(VIEW_COL_LIST_LINK),
            {
                LOCATION_TXT: self.MSK_LOCATION_NAME,
                ROOM_TYPE_TXT: ColivingTypes.ROOM,
                MIN_PRC_TXT: Restrictions.PRICE_MIN,
                MAX_PRC_TXT: Restrictions.PRICE_MIN + 1,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    ID_TXT: 1,
                    HOST_TXT: self.OWNER_1_TELEGRAM_ID,
                    LOCATION_TXT: self.MSK_LOCATION_NAME,
                    PRC_TXT: Restrictions.PRICE_MIN,
                    ROOM_TYPE_TXT: ColivingTypes.ROOM,
                    ABOUT_TXT: self.OWNER_1_ABOUT,
                    "is_visible": True,
                    "images": [],
                }
            ],
        )
        self.assertEqual(len(response.data), 1)

    def test_filters_owner_coliving(self):
        """Тест на фильтрацию данных Coliving по полю owner."""
        response = self.client.get(
            reverse(VIEW_COL_LIST_LINK),
            {"owner": self.OWNER_2_TELEGRAM_ID},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(
                coliving[HOST_TXT] == self.OWNER_2_TELEGRAM_ID
                for coliving in response.data
            ),
            "В ответе нет коливингов для указанного владельца.",
        )
        self.assertTrue(
            any(coliving[IS_VISIBLE_TXT] is False for coliving in response.data),
            msg=(
                "Если данные фильтруются по полю owner,"
                " то в выдаче должны присутствовать все коливинги пользователя."
                " Даже если установлен is_visible=False."
            ),
        )
        self.assertEqual(
            len(response.data),
            Coliving.objects.filter(host__telegram_id=self.OWNER_2_TELEGRAM_ID).count(),
            msg="В ответе не все коливинги для указанного владельца.",
        )


class UserResidenceUpdateAPITestCase(APITestCase):
    """
    Тестовые случаи для обновления информации о проживании пользователей.
    """

    OWNER_TELEGRAM_ID = 100
    INVALID_COLIVING_PK = 999
    LOCATION_NAME = "Москва"

    @classmethod
    def setUpTestData(cls):
        Coliving.objects.create(
            host=UserFromTelegram.objects.create(telegram_id=cls.OWNER_TELEGRAM_ID),
            price=Restrictions.PRICE_MIN,
            room_type=ColivingTypes.ROOM,
            location=Location.objects.create(name=cls.LOCATION_NAME),
        )

    def test_attach_user_to_coliving(self):
        """Тест на прикрепление пользователя к коливингу."""
        coliving = Coliving.objects.filter(
            host__telegram_id=self.OWNER_TELEGRAM_ID
        ).first()
        url = reverse(
            VIEW_USER_DET_LINK,
            kwargs={TELEGR_ID_TXT: self.OWNER_TELEGRAM_ID},
        )
        data = {RESIDENCE_TXT: coliving.id}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = UserFromTelegram.objects.get(telegram_id=self.OWNER_TELEGRAM_ID)
        self.assertEqual(user.residence.id, coliving.id)

    def test_detach_user_from_coliving(self):
        """Тест на открепление пользователя от коливинга."""
        user = UserFromTelegram.objects.get(telegram_id=self.OWNER_TELEGRAM_ID)
        user.residence = Coliving.objects.filter(
            host__telegram_id=self.OWNER_TELEGRAM_ID
        ).first()
        user.save()

        url = reverse(
            VIEW_USER_DET_LINK,
            kwargs={TELEGR_ID_TXT: self.OWNER_TELEGRAM_ID},
        )
        data = {RESIDENCE_TXT: None}
        response = self.client.patch(url, data)

        user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(user.residence)

    def test_update_with_invalid_telegram_id(self):
        """Тест обновления с невалидным telegram_id."""
        url = reverse(
            VIEW_USER_DET_LINK,
            kwargs={TELEGR_ID_TXT: self.INVALID_COLIVING_PK},
        )
        data = {RESIDENCE_TXT: 1}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_invalid_residence_id(self):
        """Тест обновления с невалидным residence_id."""
        user_telegram_id = self.OWNER_TELEGRAM_ID
        url = reverse(VIEW_USER_DET_LINK, kwargs={TELEGR_ID_TXT: user_telegram_id})
        data = {RESIDENCE_TXT: self.INVALID_COLIVING_PK}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserResidenceGetAPITestCase(APITestCase):
    """Тесты на получение коливинга пользователя, не являющегося владельцем."""

    USER_TELEGRAM_ID = 111111
    OWNER_TELEGRAM_ID = 22222
    LOCATION_NAME = "Москва"

    @classmethod
    def setUpTestData(cls):
        cls.coliving = Coliving.objects.create(
            host=UserFromTelegram.objects.create(telegram_id=cls.OWNER_TELEGRAM_ID),
            price=Restrictions.PRICE_MIN,
            room_type=ColivingTypes.ROOM,
            location=Location.objects.create(name=cls.LOCATION_NAME),
        )

    def test_get_coliving_by_user(self):
        UserFromTelegram.objects.create(
            telegram_id=self.USER_TELEGRAM_ID, residence_id=self.coliving.id
        )
        url = reverse(
            VIEW_COL_RET_LINK,
            kwargs={TELEGR_ID_TXT: self.USER_TELEGRAM_ID},
        )
        data = {RESIDENCE_TXT: self.coliving.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(self.coliving.id, response_json.get("id"))


class ColivingSearchAPITest(APITestCase):
    """Тесты проверки логики поиска коливинга."""

    URL = reverse(VIEW_COL_LIST_LINK)
    MSK_LOCATION_NAME = "Москва"
    SPB_LOCATION_NAME = "Санкт-Петербург"
    NON_EXISTING_VIEWER_ID = 20

    @classmethod
    def setUpTestData(cls):
        cls.host = UserFromTelegram.objects.create(telegram_id=5)
        cls.viewer = UserFromTelegram.objects.create(telegram_id=10)
        msk_location = Location.objects.create(name=cls.MSK_LOCATION_NAME)
        cls.viewer_profile = Profile.objects.create(
            user=cls.viewer,
            name="test",
            sex=Sex.MAN,
            age=Restrictions.AGE_MIN,
            location=msk_location,
        )
        cls.host_profile = Profile.objects.create(
            user=cls.host,
            name="test",
            sex=Sex.MAN,
            age=Restrictions.AGE_MIN,
            location=msk_location,
        )
        cls.coliving_1 = Coliving.objects.create(
            location=msk_location,
            price=Restrictions.PRICE_MAX - 1000,
            room_type=ColivingTypes.ROOM,
            host=cls.host,
        )
        cls.coliving_2 = Coliving.objects.create(
            location=msk_location,
            price=Restrictions.PRICE_MAX - 100,
            room_type=ColivingTypes.PLACE,
            host=cls.host,
        )

    def test_valid_request(self):
        response = self.client.get(
            self.URL,
            {
                LOCATION_TXT: self.MSK_LOCATION_NAME,
                MAX_PRC_TXT: Restrictions.PRICE_MAX,
                MIN_PRC_TXT: Restrictions.PRICE_MIN,
                ROOM_TYPE_TXT: self.coliving_2.room_type,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0][ID_TXT], self.coliving_2.id)

    def test_empty_result(self):
        response = self.client.get(
            self.URL,
            {
                LOCATION_TXT: self.SPB_LOCATION_NAME,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 0, f"Ожидался пустой список, получено: {response.data}"
        )

    def test_hosted_coliving_absent(self):
        params = {
            LOCATION_TXT: self.coliving_1.location.name,
            MAX_PRC_TXT: self.coliving_1.price + 1,
            MIN_PRC_TXT: self.coliving_1.price - 1,
            ROOM_TYPE_TXT: self.coliving_1.room_type,
            VIEWER_TXT: self.host.telegram_id,
        }
        response = self.client.get(
            self.URL,
            params,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            0,
            f"Был получен коливинг, который организовал viewer: {response.data}",
        )

    def test_viewed_content_absent(self):
        ColivingLike.objects.create(
            sender=self.viewer_profile, coliving=self.coliving_1
        )
        response = self.client.get(
            self.URL,
            {
                LOCATION_TXT: self.coliving_1.location.name,
                MAX_PRC_TXT: self.coliving_1.price + 1,
                MIN_PRC_TXT: self.coliving_1.price - 1,
                ROOM_TYPE_TXT: self.coliving_1.room_type,
                VIEWER_TXT: self.viewer.telegram_id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            0,
            f"Был получен уже просмотренный коливинг: {response.data}",
        )

    def test_non_existing_viewer(self):
        response = self.client.get(
            self.URL,
            {
                VIEWER_TXT: self.NON_EXISTING_VIEWER_ID,
            },
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Неверный статус при запросе с несуществующим viewer.",
        )
