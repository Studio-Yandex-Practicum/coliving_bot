from dataclasses import dataclass


@dataclass
class UserProfile:
    name: str
    sex: str
    age: int
    location: str
    about: str
    is_visible: str


@dataclass
class Location:
    id: int
    name: str
