import re

from fastapi import HTTPException

from src.presentation.mappings.cinema import CinemaDTO


def cinema_validate(dto: CinemaDTO):
    if not re.findall(r"^\w+@example|gmail|mail.com", dto.email):
        raise HTTPException(400, "Email error")

    if not re.findall(r"\d{10}", dto.phone_number):
        raise HTTPException(400, "Phone number error")

    return dto
