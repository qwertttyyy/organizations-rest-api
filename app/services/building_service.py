from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_building import building_crud
from app.models.building import Building


class BuildingService:
    """Сервис для работы со зданиями."""

    def __init__(self, session: AsyncSession) -> None:
        """Создает экземпляр сервиса.

        Args:
            session: Асинхронная сессия БД.
        """
        self.session = session

    async def list(self, skip: int, limit: int) -> Sequence[Building]:
        """Возвращает список зданий с пагинацией.

        Args:
            skip: Смещение.
            limit: Лимит записей.

        Returns:
            Последовательность зданий.
        """
        return await building_crud.list(self.session, skip=skip, limit=limit)
