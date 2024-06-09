from dataclasses import asdict
from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.tag import Tag
from src.presentation.mappings.tag import TagDto
from src.repository.tag_repository import TagRepository
from src.service.exceptions.exc import ValidationError
from src.service.tag_service import TagService


class TagServiceImpl(TagService):

    def __init__(self, repo: TagRepository) -> None:
        self.repo = repo

    async def create_tag(self, tag_info: TagDto, session: AsyncSession) -> int:
        tag = self.validate_tag(tag_info)
        return await self.repo.create(Tag(title=tag.get("title")), session)

    async def fetch_tags(self, session: AsyncSession) -> list[Tag]:
        return await self.repo.find_all(session)

    async def fetch_tag_info(
        self, tag_info: Union[str, int], session: AsyncSession
    ) -> Optional[Tag]:
        return await self.repo._find_by_field(tag_info, session)

    async def update_tag(
        self, tag_id: int, tag_info: TagDto, session: AsyncSession
    ) -> Tag:
        tag = self.validate_tag(tag_info)
        return await self.repo.update(tag_id, tag.get("title"), session)

    async def drop_tag(self, tag_id: int, session: AsyncSession) -> None:
        return await self.repo.delete(tag_id, session)

    @classmethod
    def validate_tag(cls, tag: TagDto) -> dict:
        errors = {}

        if len(tag.title) > 50 or len(tag.title) < 5:
            errors["length"] = (
                "Length of title must be a greaten then 5 and less then 50"
            )

        if errors:
            raise ValidationError(errors)

        tag_dict = asdict(tag)

        tag_dict["title"] = tag_dict["title"].lower()
        return tag_dict
