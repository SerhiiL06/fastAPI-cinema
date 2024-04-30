import re
from dataclasses import asdict

from fastapi import HTTPException

from src.infrastructure.database.models.cinema import Cinema
from src.presentation.mappings.cinema import CinemaDTO


def convert_cinema_dto_to_entity(dto: CinemaDTO) -> Cinema:

    if not re.findall(r"^\w+@example|gmail|mail.com", dto.email):
        raise HTTPException(400, "Email error")

    if not re.findall(r"\d{10}", dto.phone_number):
        raise HTTPException(400, "Phone number error")

    return Cinema(**asdict(dto))
