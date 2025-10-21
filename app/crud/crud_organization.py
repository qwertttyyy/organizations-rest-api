from typing import Sequence

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.core.crud_base import CRUDBase
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization


class CRUDOrganization(CRUDBase[Organization]):
    """CRUD для организаций."""

    async def by_building(
        self, session: AsyncSession, building_id: int, skip: int, limit: int
    ) -> Sequence[Organization]:
        """Возвращает организации по зданию.

        Args:
            session: Асинхронная сессия БД.
            building_id: Идентификатор здания.
            skip: Смещение.
            limit: Количество записей.

        Returns:
            Последовательность организаций.
        """
        stmt = (
            select(Organization)
            .where(Organization.building_id == building_id)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
            .order_by(Organization.id)
            .offset(skip)
            .limit(limit)
        )
        res = await session.execute(stmt)
        return list(res.scalars().unique().all())

    async def by_activity(
        self, session: AsyncSession, activity_id: int, skip: int, limit: int
    ) -> Sequence[Organization]:
        """Возвращает организации по идентификатору вида деятельности.

        Args:
            session: Асинхронная сессия БД.
            activity_id: Идентификатор вида деятельности.
            skip: Смещение.
            limit: Количество записей.

        Returns:
            Последовательность организаций.
        """
        stmt = (
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id == activity_id)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
            .order_by(Organization.id)
            .offset(skip)
            .limit(limit)
        )
        res = await session.execute(stmt)
        return list(res.scalars().unique().all())

    async def by_area(
        self,
        session: AsyncSession,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        skip: int,
        limit: int,
    ) -> Sequence[Organization]:
        """Возвращает организации по координатам прямоугольной области.

        Args:
            session: Асинхронная сессия БД.
            lat1: Нижняя широта.
            lon1: Левая долгота.
            lat2: Верхняя широта.
            lon2: Правая долгота.
            skip: Смещение.
            limit: Количество записей.

        Returns:
            Последовательность организаций.
        """
        stmt = (
            select(Organization)
            .join(Organization.building)
            .where(
                and_(
                    Building.latitude.between(lat1, lat2),
                    Building.longitude.between(lon1, lon2),
                )
            )
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
            .order_by(Organization.id)
            .offset(skip)
            .limit(limit)
        )
        res = await session.execute(stmt)
        return list(res.scalars().unique().all())

    async def search_by_name(
        self, session: AsyncSession, name: str, skip: int, limit: int
    ) -> Sequence[Organization]:
        """Возвращает организации по фрагменту названия, без учета регистра.

        Args:
            session: Асинхронная сессия БД.
            name: Фрагмент названия.
            skip: Смещение.
            limit: Количество записей.

        Returns:
            Последовательность организаций.
        """
        stmt = (
            select(Organization)
            .where(func.lower(Organization.name).ilike(f"%{name.lower()}%"))
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
            .order_by(Organization.id)
            .offset(skip)
            .limit(limit)
        )
        res = await session.execute(stmt)
        return list(res.scalars().unique().all())

    async def get_detail(
        self, session: AsyncSession, organization_id: int
    ) -> Organization | None:
        """Возвращает детальную информацию об организации.

        Args:
            session: Асинхронная сессия БД.
            organization_id: Идентификатор организации.

        Returns:
            Объект Organization или None.
        """
        stmt = (
            select(Organization)
            .where(Organization.id == organization_id)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
        )
        res = await session.execute(stmt)
        return res.scalar_one_or_none()


organization_crud = CRUDOrganization(Organization)
