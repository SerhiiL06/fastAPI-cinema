from dataclasses import asdict
from datetime import datetime

from fastapi import HTTPException

from src.presentation.mappings.actor import CreateActorDto
from src.repository.actor_repository import ActorRepository


class ActorService:
    def __init__(self, repository: ActorRepository) -> None:
        self.repo = repository

    async def fetch_all(self):
        return await self.repo.find_all()

    async def fetch_by_id(self, actor_id: int):
        return await self.repo.find_by_id(actor_id)

    async def add_actor(self, data: CreateActorDto):
        validate_data = self._actor_validate(data)
        actor_id = await self.repo.create(asdict(validate_data))

        return {"id": actor_id}

    @classmethod
    def _actor_validate(cls, actor: CreateActorDto) -> CreateActorDto:

        if actor.birth_day >= datetime.now().date():
            raise HTTPException(400, {"error": "incorrect date"})

        return actor
