from dataclasses import dataclass


@dataclass
class CityDTO:
    title: str


@dataclass
class UpdateCinemaDTO:
    title: str = None
    city: str = None
    street: str = None
    house_number: int = None
    phone_number: str = None


@dataclass
class ShortCinemaDTO:
    id: int
    title: str
    city: str
    street: str
    house_number: int
    phone_number: str


@dataclass
class CinemaDTO(ShortCinemaDTO):
    description: str
    email: str
