import re

from fastapi import HTTPException

from src.presentation.mappings.cinema import CinemaDTO


def cinema_validate(dto: CinemaDTO):
    exception_list = {"errors": {}}

    if not re.findall(r"^\w+@example|gmail|mail.com", dto.email):
        exception_list["errors"]["email"] = "invalid email pattern"

    if not re.findall(r"\d{10}", dto.phone_number):
        exception_list["errors"]["phone_number"] = "invalid phone number pattern"

    if exception_list.get("errors"):
        raise HTTPException(400, exception_list)

    return dto
