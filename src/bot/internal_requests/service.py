import os
from dataclasses import asdict
from urllib.parse import urljoin

from httpx import AsyncClient, Response

from .entities import ColivingProfile

INTERNAL_API_URL = os.getenv(
    "INTERNAL_API_URL", "http://127.0.0.1:8000/api/v1/"
)


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
