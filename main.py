from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Annotated
from core.database.connections import session

app = FastAPI()


@app.get("/")
async def test(sess: Annotated[AsyncSession, Depends(session)]):
    result = await sess.execute(text("SELECT VERSION()"))

    return result.scalars().all()
