from dataclasses import dataclass, field
from typing import List, Optional

from telegram import PhotoSize


@dataclass
class UserProfile:
    name: str
    sex: str
    age: int
    location: str
    about: str
    is_visible: str


@dataclass
class Image:
    file_id: str
    bytes: Optional[bytes] = field(default=None)
    photo_size: Optional[PhotoSize] = field(default=None)


@dataclass
class Coliving:
    location: str
    price: int
    room_type: str
    about: str
    id: Optional[int] = field(default=None)
    host: Optional[int] = field(default=None)
    is_visible: Optional[str] = field(default=None)
    images: Optional[List[Image]] = field(default=None)


@dataclass
class Location:
    id: int
    name: str
