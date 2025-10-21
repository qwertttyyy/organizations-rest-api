from typing import Generic, TypeVar, Any, Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    """Базовый асинхронный CRUD для моделей SQLAlchemy.

    Attributes:
        model: Класс ORM-модели.
    """

    def __init__(self, model: type[ModelType]) -> None:
        """Создает экземпляр класса.

        Args:
            model: Класс ORM-модели для CRUD-операций.
        """
        self.model = model

    async def get(self, session: AsyncSession, id_: Any) -> ModelType | None:
        """Возвращает объект по первичному ключу.

        Args:
            session: Асинхронная сессия БД.
            id_: Значение первичного ключа.

        Returns:
            Найденный объект или None.
        """
        stmt = select(self.model).where(getattr(self.model, "id") == id_)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_multi(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        order_by: InstrumentedAttribute | None = None,
    ) -> Sequence[ModelType]:
        """Возвращает коллекцию объектов с пагинацией.

        Args:
            session: Асинхронная сессия БД.
            skip: Смещение.
            limit: Лимит записей.
            order_by: Поле сортировки.

        Returns:
            Последовательность ORM-объектов.
        """
        stmt = select(self.model)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        stmt = stmt.offset(skip).limit(limit)
        res = await session.execute(stmt)
        return list(res.scalars().all())

    async def create(
        self, session: AsyncSession, obj_in: dict[str, Any]
    ) -> ModelType:
        """Создает объект в БД.

        Args:
            session: Асинхронная сессия БД.
            obj_in: Данные для вставки.

        Returns:
            Созданный ORM-объект.
        """

        obj = self.model(**obj_in)
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    async def update(
        self, session: AsyncSession, db_obj: ModelType, obj_in: dict[str, Any]
    ) -> ModelType:
        """Обновляет объект.

        Args:
            session: Асинхронная сессия БД.
            db_obj: Текущий ORM-объект.
            obj_in: Данные для обновления.

        Returns:
            Обновленный ORM-объект.
        """

        for k, v in obj_in.items():
            setattr(db_obj, k, v)
        await session.flush()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, id_: Any) -> None:
        """Удаляет объект по первичному ключу.

        Args:
            session: Асинхронная сессия БД.
            id_: Значение первичного ключа.
        """
        stmt = delete(self.model).where(getattr(self.model, "id") == id_)
        await session.execute(stmt)
