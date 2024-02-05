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
    images: list = field(default_factory=list)


@dataclass
class Location:
    id: int
    name: str
