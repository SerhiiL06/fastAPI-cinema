from datetime import datetime

from adaptix.load_error import AggregateLoadError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.movie import Actor
from src.presentation.mappings.actor import (ActorDetailDto, ActorDto,
                                             CreateActorDto)
from src.presentation.mappings.converters import dto_to_actor
from src.presentation.mappings.main import actor_mapper
from src.repository.actor_repository import ActorRepository
from src.service.exceptions.exc import ValidationError


class ActorService:
    def __init__(self, repository: ActorRepository) -> None:
        self.repo = repository

    async def fetch_all(self, session: AsyncSession):
        actors = await self.repo.find_all(session)

        return actor_mapper.dump(actors, list[ActorDto])

    async def fetch_by_id(self, actor_id: int, session: AsyncSession):
        actor = await self.repo.find_by_id(actor_id, session)

        return actor_mapper.dump(actor, ActorDetailDto)

    async def add_actor(self, data: CreateActorDto, session: AsyncSession):

        actor_data = dto_to_actor(data)

        self._validate_actor(actor_data)
        actor_id = await self.repo.create(actor_data, session)

        return {"id": actor_id}

    async def delete_actor(self, actor_id: int, session: AsyncSession) -> None:
        await self.repo.delete(actor_id, session)

    @classmethod
    def _validate_actor(cls, instance: Actor):

        errors = {}

        if instance.birth_day < datetime.now().date():
            errors["date"] = "error"

        if errors:
            raise ValidationError(errors)
