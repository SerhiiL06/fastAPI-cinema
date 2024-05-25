from fastapi import HTTPException
from redis import Redis

from src.service.redis_service import RedisService


class RedisServiceImpl(RedisService):

    def __init__(self, core: Redis) -> None:
        self.instance = core

    async def set_recovery_code(self, email: str, code: int) -> None:
        key = f"recovery:{email}"

        check = await self.instance.get(key)

        if check:
            to_exp = await self.instance.ttl(key)
            raise HTTPException(400, f"u can resend code after {to_exp} seconds")

        await self.instance.set(key, code, 600)

    async def verify_code(self, email: str, enter_code: int) -> bool:
        key = f"recovery:{email}"
        code = await self.instance.get(key)

        return code == enter_code
