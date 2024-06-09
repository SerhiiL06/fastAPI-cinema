import logging
from functools import wraps
from typing import Callable

from src.presentation.exceptions.exc import PermissionDanied


def check_role(allowed_roles: list):

    if type(allowed_roles) not in [list, tuple]:
        raise TypeError("Type of allowed roles must be a list or tuple")

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if user.get("role") not in allowed_roles:
                raise PermissionDanied()
            return await func(*args, **kwargs)

        return wrapper

    return decorator
