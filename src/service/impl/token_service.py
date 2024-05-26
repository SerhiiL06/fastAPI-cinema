import datetime as dt
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from src.infrastructure.settings import settings_factory


class TokenService:

    def create_token(self, payload: dict) -> str:

        payload["exp"] = datetime.now() + timedelta(minutes=30)
        token = jwt.encode(payload, settings_factory.key)
        return {"access_token": token, "token_type": "bearer"}

    def get_token(self, token: str) -> dict:
        try:
            user_data = jwt.decode(
                token, settings_factory.key, algorithms=["HS256"], leeway=3600
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            raise HTTPException(401, "reload session")

        self._verify_token(user_data)

        return user_data

    @classmethod
    def _verify_token(self, token_payload: dict) -> None:
        if datetime.fromtimestamp(token_payload.get("exp")) < datetime.now():
            raise jwt.exceptions.DecodeError("exp token")
