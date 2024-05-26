from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.infrastructure.database.models.base import Base


class PermissionDanied(Exception):
    pass


def permission_danied(request: Request, exc: PermissionDanied):
    error_text = "You don't have permission for this action"
    resp = JSONResponse(
        content={"code": "403", "msg": error_text},
        status_code=status.HTTP_403_FORBIDDEN,
    )
    return resp
