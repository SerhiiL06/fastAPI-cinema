from dataclasses import asdict
from datetime import datetime

from adaptix.load_error import AggregateLoadError
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.movie import Actor
from src.presentation.mappings.actor import CreateActorDto
from src.presentation.mappings.main import data_mapper
from src.repository.actor_repository import ActorRepository


class ActorService:
    def __init__(self, repository: ActorRepository) -> None:
        self.repo = repository

    async def fetch_all(self, session: AsyncSession):
        return await self.repo.find_all(session)

    async def fetch_by_id(self, actor_id: int, session: AsyncSession):
        return await self.repo.find_by_id(actor_id, session)

    async def add_actor(self, data: CreateActorDto, session: AsyncSession):
        try:
            actor_data = data_mapper.load(asdict(data), Actor)
        except AggregateLoadError as e:
            raise HTTPException(400, e.args[1][0].msg)

        actor_id = await self.repo.create(actor_data, session)

        return {"id": actor_id}

    async def delete_actor(self, actor_id: int, session: AsyncSession) -> None:
        await self.repo.delete(actor_id, session)

    @classmethod
    def _actor_validate(cls, actor: CreateActorDto) -> CreateActorDto:

        if actor.birth_day >= datetime.now().date():
            raise HTTPException(400, {"error": "incorrect date"})

        return actor
