from abc import ABC, abstractmethod


class UserService(ABC):

    @abstractmethod
    def register(self):
        raise NotImplementedError()

    @abstractmethod
    def fetch_users(self):
        raise NotImplementedError()

    @abstractmethod
    def fetch_user_info(self):
        raise NotImplementedError()

    @abstractmethod
    def profile_page(self):
        raise NotImplementedError()

    @abstractmethod
    def block_user(self):
        raise NotImplementedError()

    @abstractmethod
    def update_profile(self):
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self):
        raise NotImplementedError()
