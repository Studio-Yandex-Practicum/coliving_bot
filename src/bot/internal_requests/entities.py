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
    images: List[Image] = field(default_factory=list)
    location: Optional[str] = field(default=None)
    price: Optional[int] = field(default=None)
    room_type: Optional[str] = field(default=None)
    about: Optional[str] = field(default=None)
    id: Optional[int] = field(default=None)
    host: Optional[int] = field(default=None)
    is_visible: Optional[str] = field(default=None)


@dataclass
class Location:
    id: int
    name: str
