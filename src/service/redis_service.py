from abc import ABC, abstractmethod


class RedisService(ABC):
    @abstractmethod
    def set_recovery_code(self, email: str, code: int):
        raise NotImplementedError()
