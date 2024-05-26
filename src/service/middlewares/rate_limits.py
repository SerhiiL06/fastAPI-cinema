from contextlib import asynccontextmanager
from math import ceil

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi_limiter import FastAPILimiter

from src.infrastructure.database.redis import RedisCore
from src.presentation.dependency import Container


async def rate_limit_callback(request: Request, response: Response, pexpire: int):
    expire = ceil(pexpire / 1000)

    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        "Slow down!",
        headers={"Retry-After": str(expire)},
    )


@asynccontextmanager
@inject
async def rate_limit_lifespan(
    app: FastAPI,
    redis_conn: RedisCore = Depends(Provide[Container.redis.provided.connection]),
):
    await FastAPILimiter.init(redis_conn, http_callback=rate_limit_callback)
    yield
