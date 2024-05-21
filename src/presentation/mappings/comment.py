from dataclasses import dataclass


@dataclass
class CreateCommentDto:
    text: str
