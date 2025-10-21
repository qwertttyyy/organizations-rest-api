from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud_base import CRUDBase
from app.models.activity import Activity


class CRUDActivity(CRUDBase[Activity]):
    """CRUD для видов деятельности."""

    async def get_children(
        self, session: AsyncSession, parent_id: int
    ) -> Sequence[Activity]:
        """Возвращает дочерние виды деятельности.

        Args:
            session: Асинхронная сессия БД.
            parent_id: Идентификатор родителя.

        Returns:
            Последовательность дочерних Activity.
        """
        stmt = select(Activity).where(Activity.parent_id == parent_id)
        res = await session.execute(stmt)
        return list(res.scalars().all())


activity_crud = CRUDActivity(Activity)
