from dataclasses import dataclass, field


@dataclass
class UserProfile:
    user: int
    name: str
    sex: str
    age: int
    location: str
    about: str = field(default=None)
    is_visible: bool = field(default=True)


@dataclass
class Location:
    id: int
    name: str
