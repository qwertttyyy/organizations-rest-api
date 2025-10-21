"""Заполняет БД начальными данными"""

import asyncio

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import (
    Organization,
    OrganizationPhone,
    organization_activities,
)

BUILDINGS = [
    {"address": "Main St, 1", "latitude": 55.7512440, "longitude": 37.6184230},
    {
        "address": "River Rd, 5",
        "latitude": 55.7600000,
        "longitude": 37.6200000,
    },
    {
        "address": "Hill Ave, 10",
        "latitude": 55.7400000,
        "longitude": 37.6000000,
    },
    {
        "address": "Park Lane, 20",
        "latitude": 55.7700000,
        "longitude": 37.6300000,
    },
]

ACTIVITIES = [
    {"id": 1, "name": "Еда", "parent_id": None, "level": 1},
    {"id": 2, "name": "Мясная продукция", "parent_id": 1, "level": 2},
    {"id": 3, "name": "Молочная продукция", "parent_id": 1, "level": 2},
    {"id": 4, "name": "Технологии", "parent_id": None, "level": 1},
    {"id": 5, "name": "ПО", "parent_id": 4, "level": 2},
    {"id": 6, "name": "AI", "parent_id": 5, "level": 3},
]

ORGS = [
    {
        "name": "ООО Рога и Копыта",
        "building_addr": "Main St, 1",
        "phones": ["+7 900 000-00-01", "+7 900 000-00-02"],
        "activity_ids": [2, 3],
    },
    {
        "name": "ИП Вкусно",
        "building_addr": "River Rd, 5",
        "phones": ["+7 900 000-00-03"],
        "activity_ids": [2],
    },
    {
        "name": "ЗАО Молоко",
        "building_addr": "River Rd, 5",
        "phones": ["+7 900 000-00-04"],
        "activity_ids": [3],
    },
    {
        "name": "ООО ТехСтар",
        "building_addr": "Hill Ave, 10",
        "phones": ["+7 900 000-00-05"],
        "activity_ids": [4, 5],
    },
    {
        "name": "АО СофтХаб",
        "building_addr": "Hill Ave, 10",
        "phones": ["+7 900 000-00-06"],
        "activity_ids": [5, 6],
    },
    {
        "name": "ООО АйЛаб",
        "building_addr": "Park Lane, 20",
        "phones": ["+7 900 000-00-07"],
        "activity_ids": [6],
    },
    {
        "name": "ООО Фермер",
        "building_addr": "Main St, 1",
        "phones": ["+7 900 000-00-08"],
        "activity_ids": [2],
    },
    {
        "name": "ООО Сыроварня",
        "building_addr": "Park Lane, 20",
        "phones": ["+7 900 000-00-09"],
        "activity_ids": [3],
    },
    {
        "name": "ИП МясКо",
        "building_addr": "Main St, 1",
        "phones": ["+7 900 000-00-10"],
        "activity_ids": [2],
    },
    {
        "name": "ООО Инновации",
        "building_addr": "Park Lane, 20",
        "phones": [],
        "activity_ids": [4, 5, 6],
    },
]


async def upsert_buildings(session: AsyncSession) -> None:
    for b in BUILDINGS:
        exists = await session.execute(
            select(Building).where(Building.address == b["address"])
        )
        if exists.scalar_one_or_none() is None:
            obj = Building(
                address=b["address"],
                latitude=b["latitude"],
                longitude=b["longitude"],
            )
            session.add(obj)
    await session.flush()


async def upsert_activities(session: AsyncSession) -> None:
    for a in ACTIVITIES:
        exists = await session.execute(
            select(Activity).where(Activity.id == a["id"])
        )
        if exists.scalar_one_or_none() is None:
            obj = Activity(
                id=a["id"],
                name=a["name"],
                parent_id=a["parent_id"],
                level=a["level"],
            )
            session.add(obj)
    await session.flush()


async def upsert_organizations(session: AsyncSession) -> None:
    addr_to_building_id: dict[str, int] = {}
    rows = await session.execute(select(Building))
    for b in rows.scalars().all():
        addr_to_building_id[b.address] = b.id

    for o in ORGS:
        building_id = addr_to_building_id[o["building_addr"]]
        q = await session.execute(
            select(Organization).where(Organization.name == o["name"])
        )
        org = q.scalar_one_or_none()
        if org is None:
            org = Organization(name=o["name"], building_id=building_id)
            session.add(org)
            await session.flush()

        for ph in o["phones"]:
            exists = await session.execute(
                select(OrganizationPhone).where(
                    OrganizationPhone.phone_number == ph
                )
            )
            if exists.scalar_one_or_none() is None:
                session.add(
                    OrganizationPhone(organization_id=org.id, phone_number=ph)
                )

        for act_id in o["activity_ids"]:
            await session.execute(
                insert(organization_activities).values(
                    organization_id=org.id, activity_id=act_id
                )
            )

    await session.flush()


async def main() -> None:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await upsert_buildings(session)
            await upsert_activities(session)
            await upsert_organizations(session)


if __name__ == "__main__":
    asyncio.run(main())
