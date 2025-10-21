from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud_base import CRUDBase
from app.models.building import Building


class CRUDBuilding(CRUDBase[Building]):
    """CRUD для зданий."""

    async def list(
        self, session: AsyncSession, skip: int, limit: int
    ) -> Sequence[Building]:
        """Возвращает список зданий с пагинацией.

        Args:
            session: Асинхронная сессия БД.
            skip: Смещение.
            limit: Количество записей.

        Returns:
            Последовательность зданий.
        """
        stmt = select(Building).order_by(Building.id).offset(skip).limit(limit)
        res = await session.execute(stmt)
        return list(res.scalars().all())


building_crud = CRUDBuilding(Building)
