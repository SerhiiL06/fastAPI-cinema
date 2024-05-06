from src.repository.actor_repository import ActorRepository


class ActorService:
    def __init__(self, repository: ActorRepository) -> None:
        self.repo = repository

    async def fetch_all(self):
        return await self.repo.find_all()
