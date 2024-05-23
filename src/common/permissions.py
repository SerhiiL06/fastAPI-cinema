from functools import wraps
from typing import Callable

from src.presentation.exceptions.exc import PermissionDanied


def check_role(allowed_roles: list):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if user.get("role") not in allowed_roles:
                raise PermissionDanied()
            return await func(*args, **kwargs)

        return wrapper

    return decorator
