from redis import Redis
from redis import asyncio as aioredis


class RedisCore:

    def __init__(self, url: str) -> None:
        self._url = url

    @property
    def redis_url(self) -> str:
        return self._url

    @property
    def connection(self) -> Redis:
        return aioredis.from_url(self.redis_url)
