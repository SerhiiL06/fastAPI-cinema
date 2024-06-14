from dataclasses import dataclass
from datetime import date

from .country import CountryDto


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


@dataclass
class ActorDetailDto:
    from .movie import ShortMovieDto

    id: int
    first_name: str
    last_name: str

    birth_day: str
    country: CountryDto

    movies: list[ShortMovieDto]
