from datetime import datetime

from dataclasses import dataclass



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
    is_visible: bool
    viewers: bool
    created_date: datetime

    # Остальные атрибуты