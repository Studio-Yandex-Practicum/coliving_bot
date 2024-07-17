from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import List, Optional

from telegram import PhotoSize


@dataclass
class UsefulMaterial:
    title: str
    url: str


@dataclass
class UserProfile:
    user: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None)
    sex: Optional[str] = field(default=None)
    age: Optional[int] = field(default=None)
    location: Optional[str] = field(default=None)
    about: Optional[str] = field(default=None)
    residence: Optional[int] = field(default=None)
    has_coliving: Optional[bool] = field(default=None)
    is_visible: bool = field(default=True)
    images: list = field(default_factory=list)
    is_banned: bool = field(default=False)


@dataclass
class ShortProfileInfo:
    user: int
    name: str
    age: int


@dataclass
class Image:
    file_id: str
    bytes: Optional[bytes] = field(default=None)
    photo_size: Optional[PhotoSize] = field(default=None)


@dataclass
class Coliving:
    images: List[Image] = field(default_factory=list)
    location: Optional[str] = field(default=None)
    price: Optional[int] = field(default=None)
    room_type: Optional[str] = field(default=None)
    about: Optional[str] = field(default=None)
    id: Optional[int] = field(default=None)
    host: Optional[int] = field(default=None)
    is_visible: Optional[bool] = field(default=True)


@dataclass
class Location:
    id: int
    name: str


@dataclass
class ProfileSearchSettings:
    """Значения фильтров поиска по профилям пользователей."""

    age_min: Optional[int] = field(default=None)
    age_max: Optional[int] = field(default=None)
    location: Optional[str] = field(default=None)
    sex: Optional[str] = field(default=None)


@dataclass
class ColivingSearchSettings:
    """Значения фильтров поиска по объявлениям коливингов."""

    room_type: Optional[str] = field(default=None)
    min_price: Optional[int] = field(default=None)
    max_price: Optional[int] = field(default=None)
    location: Optional[str] = field(default=None)


class MatchStatuses(IntEnum):
    is_pending = 0
    is_matched = 1
    is_rejected = -1


class Categories(str, Enum):
    CATEGORY_SPAM = "Спам"
    CATEGORY_INCORRECT_DATA = "Не совпадают личные данные"
    CATEGORY_CHEATER = "Мошенник"
    CATEGORY_PROHIB_ACTIV = "Запрещенная деятельность"
    CATEGORY_BAD_LANG = "Оскорбления, мат"
    CATEGORY_OTHER = "Другое"


@dataclass
class ProfileLike:
    id: int
    sender: int
    receiver: int
    status: MatchStatuses


@dataclass
class ColivingLike:
    id: int
    sender: int
    coliving: int
    status: MatchStatuses


@dataclass
class Report:
    reporter: int
    reported_user: int
    text: str
    category: Categories
    screenshot: list = field(default_factory=list)
