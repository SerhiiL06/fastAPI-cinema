from abc import ABC, abstractmethod


class CommentService(ABC):

    @abstractmethod
    def add_comment(self, data: dict):
        pass

    @abstractmethod
    def delete_comment(self, comment_id: int):
        pass

    @abstractmethod
    def user_comments(self, user_id: int):
        pass
