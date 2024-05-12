from dataclasses import asdict
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.mappings.actor import CreateActorDto
from src.repository.actor_repository import ActorRepository


class ActorService:
    def __init__(self, repository: ActorRepository) -> None:
        self.repo = repository

    async def fetch_all(self, session: AsyncSession):
        return await self.repo.find_all(session)

    async def fetch_by_id(self, actor_id: int, session: AsyncSession):
        return await self.repo.find_by_id(actor_id, session)

    async def add_actor(self, data: CreateActorDto, session: AsyncSession):
        validate_data = self._actor_validate(data)
        actor_id = await self.repo.create(asdict(validate_data), session)

        return {"id": actor_id}

    async def delete_actor(self, actor_id: int, session: AsyncSession) -> None:
        await self.repo.delete(actor_id, session)

    @classmethod
    def _actor_validate(cls, actor: CreateActorDto) -> CreateActorDto:

        if actor.birth_day >= datetime.now().date():
            raise HTTPException(400, {"error": "incorrect date"})

        return actor
