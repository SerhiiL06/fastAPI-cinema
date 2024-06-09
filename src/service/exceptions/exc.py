from fastapi import Request, status
from fastapi.responses import JSONResponse


class ValidationError(Exception):

    def __init__(self, errors: dict) -> None:
        self.errors = errors


def validation_error(request: Request, exc: ValidationError):
    return JSONResponse(exc.errors, status.HTTP_400_BAD_REQUEST)
