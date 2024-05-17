import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    __SECRET_KEY = os.getenv("SECRET_KEY")

    @property
    def key(self):
        return self.__SECRET_KEY


settings_factory = Config()
