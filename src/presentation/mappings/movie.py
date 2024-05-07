from dataclasses import dataclass
from datetime import date


@dataclass
class CreateMovieDto:
    title: str
    description: str

    release_date: date
    duration: int
    country_id: int

    genres: list[str]
    actors: list[str]
