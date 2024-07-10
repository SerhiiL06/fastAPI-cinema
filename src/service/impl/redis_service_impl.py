import json
from typing import Optional

from fastapi import HTTPException
from redis import Redis
from redis.typing import ResponseT

from src.infrastructure.database.models.movie import Movie
from src.service.redis_service import RedisService


class RedisServiceImpl(RedisService):

    def __init__(self, core: Redis) -> None:
        self._instance = core

    async def get_movie_from_cache(self, movie_slug: str) -> Optional[ResponseT]:

        movie_key = f"movie:{movie_slug}"

        data = await self._instance.get(movie_key)

        return json.loads(data) if data else data

    async def get_movie_rating(self, movie_slug: str) -> Optional[float]:

        key = f"rating:{movie_slug}"

        rating = await self._instance.get(key)

        return float(rating) if rating else None

    async def set_movie_in_cache(self, movie_slug: int, data: Movie) -> None:

        movie_key = f"movie:{movie_slug}"

        movie_dict = json.dumps(self.model_to_dict(data))
        await self._instance.set(movie_key, movie_dict, 3600)

    async def set_recovery_code(self, email: str, code: int) -> None:
        key = f"recovery:{email}"

        check = await self._instance.get(key)

        if check:
            to_exp = await self._instance.ttl(key)
            raise HTTPException(400, f"u can resend code after {to_exp} seconds")

        await self._instance.set(key, code, 600)

    async def verify_code(self, email: str, enter_code: str) -> bool:
        key = f"recovery:{email}"
        code = await self._instance.get(key)

        return code.decode("ascii") == enter_code

    async def delete_key(self, key: str) -> None:
        await self._instance.delete(key)

    @classmethod
    def model_to_dict(cls, model: Movie):

        data = {}

        for column in model.__table__.columns:
            data[column.name] = str(getattr(model, column.name))

        return data
