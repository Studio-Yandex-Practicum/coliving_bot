from dataclasses import dataclass


@dataclass
class UserProfile:
    name: str
    sex: str
    age: int
    location: str
    about: str
    images: str
    telegram_id: int
