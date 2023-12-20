from datetime import datetime

from dataclasses import dataclass



@dataclass
class UserProfile:
    # telegram_id: int
    is_сoliving: True


# @dataclass
# class UserProfile:
#     name: str
#     sex: str
#     age: int
#     location: str
#     about: str
#     is_visible: bool



# @dataclass
# class UserFromTelegram:
#     telegram_id: int
#     telegram_username: str
#     name: str
#     surname: str


@dataclass
class ColivingProfile:
    roommates: str
    location: str
    price: int
    room_type: str
    about: str
    is_visible: bool
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
#     is_visible: bool
#     viewers: bool
#     created_date: datetime