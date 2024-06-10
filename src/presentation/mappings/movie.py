from dataclasses import dataclass
from datetime import date

from .actor import ActorDto, CountryDto


@dataclass
class CreateMovieDto:
    title: str
    description: str

    release_date: str
    duration: int
    country_name: str

    genres: list[str]
    actors: list[int]
    tags: list[int]


@dataclass
class UpdateMovieDto:
    title: str = None
    description: str = None

    release_date: date = None
    duration: int = None
    country_name: str = None

    genres: list[str] = None
    actors: list[int] = None


@dataclass
class MovieDto:
    id: int
    title: str
    slug: str
    description: str
    duration: int
    image: str
    actors: list[ActorDto]
    genres: list
    country: CountryDto
