from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserProfile:
    # telegram_id: int
    is_сoliving: True


@dataclass
class ColivingProfile:
    roommates: str
    location: str
    price: int
    room_type: str
    about: str
    is_visible: str
    viewers: bool
    created_date: datetime

    # Остальные атрибуты


# @dataclass
# class TestColivingProfile:
#     roommates: str
#     location: str
#     price: int
#     room_type: str
#     about: str
#     is_visible: str
#     viewers: bool
#     created_date: datetime
