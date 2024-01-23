import mimetypes
import urllib.parse
from typing import Optional

from httpx import AsyncClient, Response


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
        await self._post_request(endpoint_urn, files, data)

    async def _post_request(
        self,
        endpoint_urn: str,
        files: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> None:
        """
        Внутренний POST-запрос для создания объектов 'ProfileImage' и 'ColivingImage'.
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
