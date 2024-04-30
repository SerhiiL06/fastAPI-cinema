from dataclasses import dataclass


@dataclass
class CityDTO:
    title: str


@dataclass
class CinemaDTO:
    title: str
    description: str
    phone_number: str
    email: str
    city_id: int
    street: str
    house_number: int
