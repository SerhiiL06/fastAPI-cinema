from dataclasses import dataclass


@dataclass
class CityDTO:
    title: str


@dataclass
class ShortCinemaDTO:
    title: str
    city: str
    street: str
    house_number: int
    phone_number: str


@dataclass
class CinemaDTO:
    title: str
    description: str
    phone_number: str
    email: str
    city_id: int
    street: str
    house_number: int
