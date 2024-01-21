import mimetypes
import urllib.parse
from typing import Optional, List

from httpx import AsyncClient, Response

from .entities import Location


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
        запускает POST-запрос.
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
        await self.post_request(endpoint_urn, files, data)

    async def post_request(self, endpoint_urn: str, files: dict, data: dict) -> None:
        """
        POST-запрос для создания объектов 'ProfileImage' и 'ColivingImage'.
        """
        async with AsyncClient() as client:
            url: str = urllib.parse.urljoin(base=self.base_url, url=endpoint_urn)
            response: Response = await client.post(url=url, files=files, data=data)
            response.raise_for_status()

    async def get_locations(self) -> List[Location]:
        """
        Получение списка локаций.
        """
        endpoint_urn = "v1/locations/"
        async with AsyncClient() as client:
            url: str = urllib.parse.urljoin(base=self.base_url, url=endpoint_urn)
            response: Response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            locations = [Location(id=item['id'], name=item['name']) for item in data]
            return locations
