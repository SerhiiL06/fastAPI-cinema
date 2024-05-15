from src.repository.user_repository import UserRepository
from src.service.user_service import UserService


class UserServiceImpl(UserService):
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo
