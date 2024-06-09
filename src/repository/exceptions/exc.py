from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.infrastructure.database.models.base import Base


class DoesntExists(Exception):

    def __init__(self, model: Base, ident: int) -> None:
        self.model = model.__name__
        self.ident = ident


def doesnt_exists(request: Request, exc: DoesntExists):
    error_text = f"{exc.model} with value {exc.ident} doesnt exists"
    resp = JSONResponse(
        content={"code": "404", "msg": error_text},
        status_code=status.HTTP_404_NOT_FOUND,
    )
    return resp


class AlreadyExists(Exception):

    def __init__(self, model: Base, ident) -> None:
        self.model = model.__name__
        self.ident = ident


def already_exists(request: Request, exc: AlreadyExists):
    error_text = f"{exc.model} with value {exc.ident} already exists"
    resp = JSONResponse(
        content={"code": "400", "msg": error_text},
        status_code=status.HTTP_400_BAD_REQUEST,
    )
    return resp
