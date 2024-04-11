from dataclasses import dataclass, field
from typing import List, Optional

from telegram import PhotoSize


@dataclass
class UserProfile:
    user: int
    name: str
    sex: str
    age: int
    location: str
    about: str = field(default=None)
    is_visible: bool = field(default=True)
    images: list = field(default_factory=list)


@dataclass
class MatchedUser:
    user: int
    name: str


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
    is_visible: Optional[str] = field(default=True)


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
    cost_min: Optional[int] = field(default=None)
    cost_max: Optional[int] = field(default=None)
    location: Optional[str] = field(default=None)
