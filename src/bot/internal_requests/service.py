import mimetypes
from dataclasses import asdict
from typing import List, Optional
from urllib.parse import urlencode, urljoin

from httpx import AsyncClient, Response

from internal_requests.entities import (
    Coliving,
    ColivingSearchSettings,
    Image,
    Location,
    MatchedUser,
    ProfileSearchSettings,
    UserProfile,
)


class ColivingNotFound(Exception):
    def __init__(self, message, response):
        super().__init__(message)
        self.response = response


class APIService:
    """
    Сервис API-запросов.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url

    async def save_photo(
        self,
        telegram_id: int,
        photo_bytearray: bytearray,
        filename: str,
        file_id: str,
        coliving_id: Optional[int] = None,
    ) -> None:
        """
        Создает структуру запроса на создание объектов 'ProfileImage' и 'ColivingImage'
        отправляет POST-запрос.
        """
        endpoint_urn = (
            f"users/{telegram_id}/colivings/{coliving_id}/images/"
            if coliving_id
            else f"users/{telegram_id}/profile/images/"
        )
        files = dict(
            image=(
                filename,
                bytes(photo_bytearray),
                mimetypes.guess_type(filename, strict=True)[0],
            )
        )
        data = dict(file_id=file_id)
        await self._post_request(endpoint_urn, files, data)

    async def get_locations(self) -> List[Location]:
        """Запрос на получение списка городов."""
        response = await self._get_request("locations/")
        data = response.json()
        if not data:
            raise ValueError("Список Locations пуст, возможно, в БД не созданы записи.")
        locations = [Location(**item) for item in data]
        return locations

    async def save_coliving_info(self, coliving: Coliving) -> Coliving:
        """Запрос на сохранение коливинга в БД."""
        endpoint_urn = "colivings/"
        images = coliving.images[:5].copy()
        coliving.images.clear()
        data = asdict(coliving)
        response = await self._post_request(endpoint_urn=endpoint_urn, data=data)
        created_coliving = await self._parse_response_to_coliving(response.json())
        await self.save_coliving_photo(images, created_coliving)
        return created_coliving

    async def save_coliving_photo(self, images, coliving: Coliving) -> int:
        """Запрос на сохранение фото коливинга в БД."""
        for image in images:
            file = await image.photo_size.get_file()
            photo_bytearray = await file.download_as_bytearray()
            await self.save_photo(
                telegram_id=coliving.host,
                photo_bytearray=photo_bytearray,
                filename=file.file_path,
                file_id=image.file_id,
                coliving_id=coliving.id,
            )

    async def get_coliving_info_by_user(self, telegram_id: int) -> Coliving:
        """
        Запрос на получение информации о коливинге по ID владельца.
        :param telegram_id: Chat ID пользователя, зарегистрировавшего коливинг
        :raise ColivingNotFound: Если коливингов не нашлось
        """
        endpoint_urn = f"colivings/?owner={telegram_id}"
        response = await self._get_request(endpoint_urn=endpoint_urn)
        response_json = response.json()
        if not response_json:
            raise ColivingNotFound(
                message="Пользователь не зарегистрировал коливингов",
                response=response,
            )
        return await self._parse_response_to_coliving(response_json[0])

    async def update_coliving_info(self, coliving: Coliving) -> Coliving:
        """Запрос на частичное обновление информации по коливингу."""
        endpoint_urn = f"colivings/{coliving.id}/"
        coliving.images.clear()
        data = asdict(coliving)
        response = await self._patch_request(endpoint_urn=endpoint_urn, data=data)
        return await self._parse_response_to_coliving(response.json())

    async def update_user_residence(
        self, telegram_id: int, residence_id: Optional[int] = None
    ) -> Response:
        """
        Обновляет проживание пользователя,
        позволяя прикрепить его к коливингу или открепить.
        """
        endpoint_urn = f"users/{telegram_id}/"
        data = {"residence": residence_id}
        return await self._patch_request(endpoint_urn=endpoint_urn, data=data)

    async def get_potential_roommates(
        self,
        telegram_id: int,
    ) -> List[MatchedUser]:
        """
        Выводит список потенциальных жильцов
        для данного коливинга - всех пользователей,
        у кого есть мэтч с данным telegram_id.
        """
        endpoint_urn = f"users/{telegram_id}/matches/?roommates=1"
        response = await self._get_request(endpoint_urn=endpoint_urn)
        result = []
        for matched_user in response.json():
            result.append(MatchedUser(**matched_user))
        return result

    async def get_user_profile_by_telegram_id(
        self, telegram_id: int
    ) -> Optional[UserProfile]:
        """
        Получение профиля пользователя по идентификатору chat id.

        :param telegram_id: chat id пользователя.
        :return: Объект UserProfile или None, если профиль не найден.
        """
        response = await self._get_request(f"users/{telegram_id}/profile/")
        return UserProfile(**response.json())

    async def get_filtered_user_profiles(
        self, filters: ProfileSearchSettings, viewer: int
    ) -> List[UserProfile]:
        """
        Получение отфильтрованных анкет пользователей.

        :param filters: Значения для query-параметров поиска
        :param viewer: Telegram ID пользователя, осуществляющего поиск
        :return: Профили, подходящие по фильтрам
        """
        params_dict = {k: v for k, v in asdict(filters).items() if v is not None}
        search_params = urlencode(params_dict)
        response = await self._get_request(f"profiles/?{search_params}&viewer={viewer}")
        result = []
        for profile in response.json():
            result.append(UserProfile(**profile))
        return result

    async def get_filtered_colivings(
        self, filters: ColivingSearchSettings, viewer: int
    ) -> List[Coliving]:
        """
        Получение отфильтрованных объявлений коливинга.

        :param filters: Значения для query-параметров поиска
        :param viewer: Telegram ID пользователя, осуществляющего поиск
        :return: Коливинги, подходящие по фильтрам
        """
        params_dict = {k: v for k, v in asdict(filters).items() if v is not None}
        search_params = urlencode(params_dict)
        response = await self._get_request(
            f"colivings/?{search_params}&viewer={viewer}"
        )
        result = []
        for coliving in response.json():
            result.append(Coliving(**coliving))
        return result

    async def create_user_profile(
        self, telegram_id: int, data: dict
    ) -> Optional[UserProfile]:
        """
        Создание профиля пользователя.

        :param telegram_id: Идентификатор пользователя.
        :param data: Объект UserProfile с данными для создания профиля.
        :return: Созданный профиль или None, если что-то пошло не так.
        """
        return await self._profile_request(telegram_id, data, method="post")

    async def update_user_profile(
        self, telegram_id: int, data: dict
    ) -> Optional[UserProfile]:
        """
        Обновление профиля пользователя.

        :param telegram_id: Идентификатор пользователя.
        :param data: Словарь данных для обновления профиля.
        :return: Обновленный профиль или None, если что-то пошло не так.
        """
        return await self._profile_request(telegram_id, data, method="patch")

    async def delete_coliving(self, coliving_id: int) -> Response:
        """
        Удаляет профиль коливинга.
        """
        endpoint_urn = f"colivings/{coliving_id}/"
        return await self._delete_request(endpoint_urn)

    async def delete_coliving_photos(
        self, coliving_id: int, telegram_id: int
    ) -> Response:
        """
        Удаляет все фотографии, связанные с конкретным коливингом.
        """
        endpoint_urn = f"users/{telegram_id}/colivings/{coliving_id}/images/"
        return await self._delete_request(endpoint_urn)

    async def delete_profile_photos(self, telegram_id: int) -> Response:
        """
        Удаляет все фотографии профиля пользователя.
        """
        endpoint_urn = f"users/{telegram_id}/profile/images/"
        return await self._delete_request(endpoint_urn)

    async def send_match_request(self, sender: int, receiver: int) -> Response:
        """Совершает POST-запрос к эндпоинту создания MatchRequest.

        :param sender: telegram_id отправителя.
        :param receiver: telegram_id получателя.
        """
        endpoint_urn = "match_requests/"
        data = {"sender": sender, "receiver": receiver}
        response = await self._post_request(endpoint_urn=endpoint_urn, data=data)
        return response

    async def _profile_request(
        self, telegram_id: int, data: dict, method: str
    ) -> Optional[UserProfile]:
        """
        Основная функция для создания и обновления профиля.

        :param telegram_id: Идентификатор пользователя.
        :param data: Словарь данных для профиля.
        :param method: HTTP-метод ('post' или 'patch').
        :return: Созданный или обновленный профиль, или None, если что-то пошло не так.
        """
        endpoint_urn = f"users/{telegram_id}/profile/"
        request_data = {
            "name": data.get("name", ""),
            "sex": data.get("sex", ""),
            "age": data.get("age", 0),
            "location": data.get("location", ""),
            "about": data.get("about", ""),
            "is_visible": data.get("is_visible", True),
        }
        response = await getattr(self, f"_{method}_request")(
            endpoint_urn, data=request_data
        )
        return UserProfile(**response.json())

    async def _get_request(self, endpoint_urn: str) -> Response:
        """
        Отправляет GET-запрос к указанному эндпоинту.

        :param endpoint_urn: Относительный URI эндпоинта.
        """
        async with AsyncClient() as client:
            response = await client.get(urljoin(base=self.base_url, url=endpoint_urn))
            response.raise_for_status()
        return response

    async def _post_request(
        self,
        endpoint_urn: str,
        files: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Response:
        """
        Отправляет POST-запрос к указанному эндпоинту.

        :param endpoint_urn: Относительный URI эндпоинта.
        :param files: Опциональный параметр. Словарь файлов для отправки
        (в формате {'file_field_name': ('filename', bytes, 'content_type')}).
        :param data: Опциональный параметр. Словарь данных для отправки в формате JSON.
        """
        async with AsyncClient() as client:
            url: str = urljoin(base=self.base_url, url=endpoint_urn)
            if files:
                response = await client.post(url=url, files=files, data=data)
            elif data:
                response = await client.post(url=url, json=data)
            else:
                raise ValueError("Оба значения 'files' и 'data' не могут быть None.")
            response.raise_for_status()
        return response

    async def _patch_request(self, endpoint_urn: str, data: dict) -> Response:
        """
        Отправляет PATCH-запрос к указанному эндпоинту.

        :param endpoint_urn: Относительный URI эндпоинта.
        :param data: Словарь данных для отправки в формате JSON.
        """
        async with AsyncClient() as client:
            response = await client.patch(
                url=urljoin(
                    base=self.base_url,
                    url=endpoint_urn,
                ),
                json=data,
            )
        response.raise_for_status()
        return response

    async def _delete_request(self, endpoint_urn: str) -> Response:
        """
        Отправляет DELETE-запрос к указанному эндпоинту.

        :param endpoint_urn: Относительный URI эндпоинта.
        """
        async with AsyncClient() as client:
            response = await client.delete(
                urljoin(base=self.base_url, url=endpoint_urn)
            )
            response.raise_for_status()
        return response

    @staticmethod
    async def _parse_response_to_coliving(response_json: object) -> Coliving:
        """Парсит полученный json, упаковывая в датакласс Coliving."""
        if not isinstance(response_json, dict):
            raise ValueError(
                "Возможно было получено несколько записей, ожидалась одна."
            )
        images = response_json.pop("images")
        coliving_info = Coliving(**response_json)
        if images:
            coliving_info.images = [Image(file_id=file_id) for file_id in images]
        return coliving_info
