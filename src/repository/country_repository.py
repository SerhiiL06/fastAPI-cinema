from typing import Optional, Union

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.movie import Country


class CountryRepository:

    async def find_by_name_or_iso(
        self, county_name: Union[str, list], session: AsyncSession
    ) -> Optional[Union[Country, list[Country]]]:

        q = select(Country)

        if isinstance(county_name, list):
            q = q.where(
                or_(Country.name.in_(county_name), Country.iso.in_(county_name))
            )
        else:

            q = q.where(
                or_(
                    Country.name.icontains(county_name),
                    Country.iso.icontains(county_name),
                )
            )

        result = await session.execute(q)

        return result.scalars().first()

    async def find_country_by_id(
        self, country_id: int, session: AsyncSession
    ) -> Optional[Country]:

        q = select(Country).where(Country.id == country_id)

        result = await session.execute(q)

        return result.scalars().one_or_none()
