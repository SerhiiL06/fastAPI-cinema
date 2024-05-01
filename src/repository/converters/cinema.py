import re
from dataclasses import asdict

from fastapi import HTTPException

from src.infrastructure.database.models.cinema import Cinema
from src.presentation.mappings.cinema import CinemaDTO, ShortCinemaDTO


def cinema_dto_to_entity(dto: CinemaDTO) -> Cinema:

    return Cinema(**asdict(dto))


def cinema_entity_to_dto(
    entity: list[Cinema] | Cinema,
) -> list[CinemaDTO] | CinemaDTO:

    if isinstance(entity, list):
        list_dtos = []

        for ent in entity:
            list_dtos.append(
                ShortCinemaDTO(
                    id=ent.id,
                    title=ent.title,
                    city=ent.city.title,
                    street=ent.street,
                    house_number=ent.house_number,
                    phone_number=ent.phone_number,
                )
            )

        return list_dtos
    return CinemaDTO(**entity)
