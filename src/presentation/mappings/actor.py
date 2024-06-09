from dataclasses import dataclass
from datetime import date


@dataclass
class CreateActorDto:
    first_name: str
    last_name: str

    birth_day: str
    country_id: int
