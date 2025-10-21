from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import get_db


async def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Проверяет валидность API-ключа.

    Args:
        x_api_key: Значение заголовка X-API-Key.

    Raises:
        HTTPException: Если ключ не предоставлен или неверен.
    """
    if not x_api_key or x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный API ключ",
        )


async def get_session() -> AsyncSession:
    """Возвращает асинхронную сессию БД.

    Returns:
        Асинхронная сессия SQLAlchemy.
    """
    async for s in get_db():
        return s
