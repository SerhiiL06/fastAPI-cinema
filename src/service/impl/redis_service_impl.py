from fastapi import HTTPException
from redis import Redis

from src.service.redis_service import RedisService


class RedisServiceImpl(RedisService):

    def __init__(self, core: Redis) -> None:
        self._instance = core

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
