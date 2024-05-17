from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connections import session_transaction
from src.presentation.dependency import Container

session_factory = Annotated[AsyncSession, Depends(session_transaction)]
current_user = Annotated[dict, Depends(Container.auth_service().authenticate)]
