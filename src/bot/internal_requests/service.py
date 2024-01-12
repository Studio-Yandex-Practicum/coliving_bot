import mimetypes
import os
import urllib.parse
from dataclasses import asdict
from typing import Optional
from urllib.parse import urljoin

from httpx import AsyncClient, Response

from .entities import ColivingProfile

INTERNAL_API_URL = os.getenv("INTERNAL_API_URL", "http://127.0.0.1:8000/api/v1/")


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


async def create_coliving(coliving: ColivingProfile) -> Response:
    """Запрос на занесение пользователя в БД."""
    data = asdict(coliving)
    endpoint_urn = "coliving/"
    response = await _post_request(data, endpoint_urn)
    return response


async def update_coliving_info(telegram_id: int, data: dict):
    endpoint_run = f"coliving/{telegram_id}/"
    response = await _patch_request(data, endpoint_run)
    user_info_updated = await _parse_api_response_to_coliving_info(response)
    return user_info_updated


async def _parse_api_response_to_coliving_info(
    response: Response,
) -> ColivingProfile:
    """Парсит полученный json из Response в датакласс ColivingProfile."""
    return ColivingProfile(**response.json())


async def _post_request(data: dict, endpoint_url: str) -> Response:
    async with AsyncClient() as client:
        response = await client.post(
            url=urljoin(
                base=INTERNAL_API_URL,
                url=endpoint_url,
            ),
            json=data,
        )
    response.raise_for_status()
    return response


async def _patch_request(data: dict, endpoint_url: str) -> Response:
    async with AsyncClient() as client:
        response = await client.patch(
            url=urljoin(
                base=INTERNAL_API_URL,
                url=endpoint_url,
            ),
            json=data,
        )
    response.raise_for_status()
    return response
