import mimetypes
import urllib.parse
from typing import List, Optional

from httpx import AsyncClient, HTTPError, Response

from internal_requests.entities import Location, UserProfile


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
        files = {
            "image": (
                filename,
                bytes(photo_bytearray),
                mimetypes.guess_type(filename, strict=True)[0],
            )
        }
        data = dict(file_id=file_id)
        await self._post_request(endpoint_urn, files, data)

    async def get_locations(self) -> List[Location]:
        """
        Получение списка локаций.
        """
        response = await self._get_request("locations/")
        data = response.json()
        locations = [Location(id=item["id"], name=item["name"]) for item in data]
        return locations

    async def get_user_profile_by_telegram_id(
        self, telegram_id: int
    ) -> Optional[UserProfile]:
        """
        Получение профиля пользователя по идентификатору телеграма.

        :param telegram_id: Идентификатор телеграма пользователя.
        :return: Объект UserProfile или None, если профиль не найден.
        """
        try:
            response = await self._get_request(f"users/{telegram_id}/profile/")
            if response.status_code == 200:
                data = response.json()
                return UserProfile(**data)
            else:
                return None
        except HTTPError as exc:
            print(f"Профиль не найден: {exc}")
            return None

    async def create_user_profile(
        self, telegram_id: int, data: dict
    ) -> Optional[UserProfile]:
        """
        Создание профиля пользователя.

        :param telegram_id: Идентификатор пользователя.
        :param data: Объект UserProfile с данными для создания профиля.
        :return: Созданный профиль или None, если что-то пошло не так.
        """
        endpoint_urn = f"users/{telegram_id}/profile/"
        request_data = {
            "name": data.get("name", ""),
            "sex": data.get("sex", "").replace("🚺", ""),
            "age": data.get("age", 0),
            "location": data.get("location", ""),
            "about": data.get("about", ""),
            "is_visible": data.get("is_visible", True),
        }
        response = await self._post_request(endpoint_urn, data=request_data)
        if response.status_code == 201:
            created_profile_data = response.json()
            return UserProfile(**created_profile_data)
        else:
            print(f"Ошибка создания профиля. Status code: {response.status_code}")
            return None

    async def update_user_profile(
        self, telegram_id: int, data: dict
    ) -> Optional[UserProfile]:
        """
        Обновление профиля пользователя.

        :param telegram_id: Идентификатор пользователя.
        :param data: Словарь данных для обновления профиля.
        :return: Обновленный профиль или None, если что-то пошло не так.
        """
        try:
            endpoint_urn = f"users/{telegram_id}/profile/"
            response = await self._patch_request(endpoint_urn, data=data)

            if response.status_code == 200:
                updated_profile_data = response.json()
                return UserProfile(**updated_profile_data)
            else:
                print(f"Ошибка обновления профиля. Status code: {response.status_code}")
                return None
        except HTTPError as exc:
            print(f"Ошибка обновления профиля: {exc}")
            return None

    async def _post_request(
        self,
        endpoint_urn: str,
        files: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Response:
        """
        Асинхронно отправляет POST-запрос к указанному эндпоинту.

        :param endpoint_urn: Относительный URI эндпоинта.
        :param files: Опциональный параметр. Словарь файлов для отправки
        (в формате {'file_field_name': ('filename', bytes, 'content_type')}).
        :param data: Опциональный параметр. Словарь данных для отправки в формате JSON.
        """
        async with AsyncClient() as client:
            url: str = urllib.parse.urljoin(base=self.base_url, url=endpoint_urn)
            if files:
                response: Response = await client.post(url=url, files=files, data=data)
            elif data:
                response: Response = await client.post(url=url, json=data)
            else:
                raise ValueError("Оба значения 'files' и 'data' не могут быть None.")
            response.raise_for_status()
        return response

    async def _get_request(self, endpoint_urn: str) -> Response:
        """
        Асинхронно отправляет GET-запрос к указанному эндпоинту.
        """
        async with AsyncClient() as client:
            url: str = urllib.parse.urljoin(base=self.base_url, url=endpoint_urn)
            response: Response = await client.get(url)
            response.raise_for_status()
        return response

    async def _patch_request(
        self,
        endpoint_urn: str,
        data: Optional[dict] = None,
    ) -> Response:
        """
        Асинхронно отправляет PATCH-запрос к указанному эндпоинту.

        :param endpoint_urn: Относительный URI эндпоинта.
        :param data: Опциональный параметр. Словарь данных для отправки в формате JSON.
        """
        async with AsyncClient() as client:
            url: str = urllib.parse.urljoin(base=self.base_url, url=endpoint_urn)
            response: Response = await client.patch(url=url, json=data)
            response.raise_for_status()
        return response
