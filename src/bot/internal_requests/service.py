import mimetypes
from dataclasses import asdict
from typing import List, Optional
from urllib.parse import urljoin

from httpx import AsyncClient, Response

from internal_requests.entities import Coliving, Image, Location


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
        images = coliving.images.copy()
        coliving.images.clear()
        data = asdict(coliving)
        response = await self._post_request(endpoint_urn=endpoint_urn, data=data)
        created_coliving = await self._parse_response_to_coliving(response.json())
        for image in images:
            file = await image.photo_size.get_file()
            photo_bytearray = await file.download_as_bytearray()
            await self.save_photo(
                telegram_id=created_coliving.host,
                photo_bytearray=photo_bytearray,
                filename=file.file_path,
                file_id=image.file_id,
                coliving_id=created_coliving.id,
            )
            created_coliving.images.append(Image(file_id=image.file_id))
        return created_coliving

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

    async def _get_request(self, endpoint_urn: str) -> Response:
        """
        Отправляет GET-запрос к указанному эндпоинту.
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

    @staticmethod
    async def _parse_response_to_coliving(response_json: object) -> Coliving:
        """Парсит полученный json, упаковывая в датакласс Coliving."""
        if not isinstance(response_json, dict):
            ValueError("Возможно было получено несколько записей, ожидалась одна.")
        images = response_json.pop("images")
        coliving_info = Coliving(**response_json)
        if images:
            coliving_info.images = [Image(file_id=file_id) for file_id in images]
        return coliving_info
