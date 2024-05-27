from abc import ABC, abstractmethod


class EmailService(ABC):

    @abstractmethod
    def send_verificated_message(self, address: str):
        raise NotImplementedError()

    @abstractmethod
    def send_recovery_code(self, address: str):
        raise NotImplementedError()
