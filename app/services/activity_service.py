from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_activity import activity_crud
from app.models.activity import Activity


class ActivityService:
    """Сервис для работы с видами деятельности."""

    def __init__(self, session: AsyncSession) -> None:
        """Создает экземпляр сервиса.

        Args:
            session: Асинхронная сессия БД.
        """
        self.session = session

    async def validate_level(self, level: int) -> None:
        """Проверяет корректность уровня.

        Args:
            level: Уровень вложенности.

        Raises:
            ValueError: Если уровень некорректен.
        """
        if level < 1 or level > 3:
            raise ValueError("Activity level must be between 1 and 3")

    async def get_all_descendants_ids(self, activity_id: int) -> list[int]:
        """Возвращает идентификаторы всех дочерних видов деятельности.

        Args:
            activity_id: Идентификатор корневой деятельности.

        Returns:
            Список идентификаторов всех потомков, включая исходный.
        """
        collected: set[int] = set()

        async def _collect(aid: int) -> None:
            collected.add(aid)
            children: Sequence[Activity] = await activity_crud.get_children(
                self.session, aid
            )
            for c in children:
                await _collect(c.id)

        await _collect(activity_id)
        return list(collected)
