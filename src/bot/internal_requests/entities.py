from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserProfileTest:
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
