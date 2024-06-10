from dataclasses import dataclass
from datetime import date


@dataclass
class CountryDto:
    id: int
    name: str


@dataclass
class CreateActorDto:
    first_name: str
    last_name: str
    birth_day: date
    country_id: int


@dataclass
class ActorDto:
    id: int
    first_name: str
    last_name: str

    birth_day: str
    country: CountryDto
