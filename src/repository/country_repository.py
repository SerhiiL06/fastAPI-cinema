from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from src.infrastructure.database.models.movie import Country
from src.repository.abstract import AbstractRepository


class CountryRepository:

    async def country_by_title(
        self, county_name: Union[str, list], session: AsyncSession
    ) -> Optional[Union[Country, list[Country]]]:

        q = select(Country)

        if isinstance(county_name, list):
            q = q.where(Country.name.in_(county_name))
        else:

            q = q.where(Country.name.icontains(county_name))

        result = await session.execute(q)

        return result.scalars().one_or_none()

    async def country_by_id(
        self, country_id: int, session: AsyncSession
    ) -> Optional[Country]:

        q = select(Country).where(Country.id == country_id)

        result = await session.execute(q)

        return result.scalars().one_or_none()
