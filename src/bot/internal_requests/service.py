import mimetypes
from dataclasses import asdict
from typing import List, Optional
from urllib.parse import urlencode, urljoin

from httpx import AsyncClient, Response

from internal_requests.entities import (
    Coliving,
    ColivingLike,
    ColivingSearchSettings,
    Image,
    Location,
    ProfileLike,
    ProfileSearchSettings,
    Report,
    ShortProfileInfo,
    UsefulMaterial,
    UserProfile,
)


class APIService:
    """
    Сервис API-запросов.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url

    async def create_report(self, report: Report) -> Response:
        """
        Запрос на создание жалобы на пользователя.
        """
        endpoint_urn = "reports/"
        data = asdict(report)
        data["category"] = data["category"].value
        image = data.pop("screenshot")
        if image:
            image = image["photo_size"]
            image_file = await image.get_file()
            photo_bytearray = await image_file.download_as_bytearray()
            files = {
                "screenshot": (
                    image_file.file_path,
                    bytes(photo_bytearray),
                    mimetypes.guess_type(image_file.file_path, strict=True)[0],
                )
            }
            response = await self._post_request(
                endpoint_urn=endpoint_urn, data=data, files=files
            )
            return response
        response = await self._post_request(endpoint_urn=endpoint_urn, data=data)
        return response

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

    async def save_profile_photo(self, images, profile: UserProfile) -> None:
        """Запрос на сохранение фото коливинга в БД."""
        for image in images:
            file = await image.photo_size.get_file()
            photo_bytearray = await file.download_as_bytearray()
            await self.save_photo(
                telegram_id=profile.user,
                photo_bytearray=photo_bytearray,
                filename=file.file_path,
                file_id=image.file_id,
            )

    async def save_coliving_photo(self, images, coliving: Coliving) -> None:
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
        Возвращает коливинг пользователя.
        """
        endpoint_urn = f"colivings/?owner={telegram_id}"
        response = await self._get_request(endpoint_urn)
        response_json = response.json()
        if response_json:
            return await self._parse_response_to_coliving(response_json[0])
        endpoint_urn = f"users/{telegram_id}/residence"
        response = await self._get_request(endpoint_urn)
        response_json = response.json()
        return await self._parse_response_to_coliving(response_json)

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

    async def get_matched_coliving_likes(
        self,
        coliving_pk: int,
    ) -> List[ShortProfileInfo]:
        """
        Выводит одобренные (is_matched) лайки для переданного коливинга.
        """
        endpoint_urn = f"colivings/{coliving_pk}/matches/"
        response = await self._get_request(endpoint_urn=endpoint_urn)
        result = []
        for matched_user in response.json():
            result.append(ShortProfileInfo(**matched_user))
        return result

    async def get_matched_profile_likes(
        self,
        telegram_id: int,
    ) -> List[ShortProfileInfo]:
        """
        Выводит совпадающие (is_matched) лайки для переданного пользователя.
        """
        endpoint_urn = f"users/{telegram_id}/matches/?roommates=1"
        response = await self._get_request(endpoint_urn=endpoint_urn)
        result = []
        for matched_user in response.json():
            result.append(ShortProfileInfo(**matched_user))
        return result

    async def send_profile_like(
        self, sender: int, receiver: int, status: Optional[int] = None
    ) -> ProfileLike:
        """Отправляет запрос на создание лайка профиля."""
        endpoint_urn = "profiles/like/"
        data = {"sender": sender, "receiver": receiver}
        if status is not None:
            data["status"] = status
        response = await self._post_request(endpoint_urn=endpoint_urn, data=data)
        return ProfileLike(**response.json())

    async def update_status_profile_like(self, pk: int, status: int) -> ProfileLike:
        """Отправляет запрос на обновление статуса лайка профиля."""
        endpoint_urn = f"profiles/like/{pk}/"
        data = {"status": status}
        response = await self._patch_request(endpoint_urn=endpoint_urn, data=data)
        return ProfileLike(**response.json())

    async def send_coliving_like(
        self, sender: int, coliving_pk: int, status: Optional[int] = None
    ) -> ColivingLike:
        """Отправляет запрос на создание лайка для коливинга."""
        endpoint_urn = "colivings/like/"
        data = {"sender": sender, "coliving": coliving_pk}
        if status is not None:
            data["status"] = status
        response = await self._post_request(endpoint_urn=endpoint_urn, data=data)
        return ColivingLike(**response.json())

    async def update_status_coliving_like(self, pk: int, status: int) -> ColivingLike:
        """Отправляет запрос на обновление статуса лайка для коливинга."""
        endpoint_urn = f"colivings/like/{pk}/"
        data = {"status": status}
        response = await self._patch_request(endpoint_urn=endpoint_urn, data=data)
        return ColivingLike(**response.json())

    async def get_user_profile_by_telegram_id(
        self, telegram_id: int
    ) -> Optional[UserProfile]:
        """
        Получение профиля пользователя по идентификатору chat id.

        :param telegram_id: chat id пользователя.
        :return: Объект UserProfile или None, если профиль не найден.
        """
        response = await self._get_request(f"users/{telegram_id}/profile/")
        return await self._parse_response_to_user_profile(response.json())

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
            parsed_profile = await self._parse_response_to_user_profile(profile)
            result.append(parsed_profile)
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
            parsed_coliving = await self._parse_response_to_coliving(coliving)
            result.append(parsed_coliving)
        return result

    async def get_coliving_roommates(self, coliving_id: int, page: int) -> dict:
        """Получение списка соседей."""
        response = await self._get_request(
            f"colivings/{coliving_id}/roommates/?page={page}"
        )
        return response.json()

    async def create_user_profile(self, profile: UserProfile) -> Optional[UserProfile]:
        """
        Создание профиля пользователя.

        :param profile: Объект UserProfile с данными для создания профиля.
        :return: Созданный профиль
        """

        endpoint_urn = f"users/{profile.user}/profile/"
        images = profile.images.copy()
        profile.images.clear()
        data = asdict(profile)
        response = await self._post_request(endpoint_urn=endpoint_urn, data=data)
        created_profile = await self._parse_response_to_user_profile(response.json())
        await self.save_profile_photo(images, created_profile)
        return created_profile

    async def delete_profile(self, telegram_id: int) -> Response:
        """
        Удаляет профиль пользователя.
        """
        endpoint_urn = f"users/{telegram_id}/profile/"
        return await self._delete_request(endpoint_urn)

    async def update_user_profile(self, profile: UserProfile) -> UserProfile:
        """
        Обновление профиля пользователя.

        :param profile: Данные для обновления профиля.
        :return: Обновленный профиль
        """
        endpoint_urn = f"users/{profile.user}/profile/"
        profile.images.clear()
        data = asdict(profile)
        response = await self._patch_request(endpoint_urn=endpoint_urn, data=data)
        return await self._parse_response_to_user_profile(response.json())

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

    async def get_potential_roommates(self, coliving_pk: int) -> List[UserProfile]:
        endpoint_urn = f"colivings/{coliving_pk}/potential-roommates/"
        response = await self._get_request(endpoint_urn)
        result = []
        for profile in response.json():
            parsed_profile = await self._parse_response_to_user_profile(profile)
            result.append(parsed_profile)
        return result

    async def delete_old_likes(self):
        """Отправляет запросы на удаление лайков"""
        profile_endpoint_urn = "profiles/like/delete_old_likes/"
        coliving_endpoint_urn = "colivings/like/delete_old_likes/"

        profile_response = await self._delete_request(profile_endpoint_urn)
        coliving_response = await self._delete_request(coliving_endpoint_urn)

        return {
            "profile_response": profile_response,
            "coliving_response": coliving_response,
        }

    async def get_mailing(self) -> Optional[dict]:
        """
        Получение сообщения для рассылки.
        """
        endpoint_urn = "mailings/"
        response = await self._get_request(endpoint_urn)
        if response.json():
            return response.json()[-1]
        return None

    async def get_users_for_mailing(self, page: int) -> List[int]:
        """
        Получение списка пользователей для рассылки.

        :param page: значение страницы.
        """
        endpoint_urn = f"mailings/users/?page={page}"
        response = await self._get_request(endpoint_urn)
        return response.json()

    async def update_mail(self, mailing_id, status):
        """
        Обновление поля 'status' у рассылки.

        :param mailing_id: id рассылки для обновления.
        :param status: статус сообщения рассылки.
        """
        endpoint_urn = f"mailings/{mailing_id}/"
        await self._patch_request(endpoint_urn=endpoint_urn, data={"status": status})

    async def get_useful_materials(self) -> List[UsefulMaterial]:
        """
        Получение списка полезных материалов.

        :return: Список объектов UsefulMaterial.
        """
        response = await self._get_request("useful-materials/")
        materials_json = response.json()

        useful_materials = []
        for material in materials_json:
            useful_materials.append(UsefulMaterial(**material))

        return useful_materials

    async def _get_request(self, endpoint_urn: str) -> Response:
        """
        Отправляет GET-запрос к указанному эндпоинту.

        :param endpoint_urn: Относительный URI эндпоинта.
        """
        async with AsyncClient() as client:
            response = await client.get(
                urljoin(base=self.base_url, url=endpoint_urn), follow_redirects=True
            )
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

    @staticmethod
    async def _parse_response_to_user_profile(response_json: object) -> UserProfile:
        if not isinstance(response_json, dict):
            raise ValueError(
                "Возможно было получено несколько записей, ожидалась одна."
            )
        images = response_json.pop("images")
        profile_info = UserProfile(**response_json)
        if images:
            profile_info.images = [Image(file_id=file_id) for file_id in images]
        return profile_info
