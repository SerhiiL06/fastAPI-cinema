import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

load_dotenv()


class Config:
    _SECRET_KEY = os.getenv("SECRET_KEY")
    _MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    _MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    _MAIL_PORT = os.getenv("MAIL_PORT")
    _MAIL_SERVER = os.getenv("MAIL_SERVER")

    @property
    def key(self):
        return self._SECRET_KEY

    @property
    def email_config(self) -> ConnectionConfig:
        print(self._MAIL_PASSWORD)
        config = ConnectionConfig(
            MAIL_USERNAME=self._MAIL_USERNAME,
            MAIL_PASSWORD=self._MAIL_PASSWORD,
            MAIL_PORT=self._MAIL_PORT,
            MAIL_SERVER=self._MAIL_SERVER,
            MAIL_FROM=self._MAIL_USERNAME,
            MAIL_SSL_TLS=True,
            MAIL_STARTTLS=False,
        )

        return config


settings_factory = Config()
