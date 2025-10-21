from datetime import datetime

from pydantic import BaseModel, field_validator


class ActivityBase(BaseModel):
    """Базовые поля вида деятельности."""

    id: int
    name: str
    parent_id: int | None
    level: int

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: int) -> int:
        """Проверяет допустимый уровень."""
        if v < 1 or v > 3:
            raise ValueError("Уровень должен быть от 1 до 3")
        return v


class ActivityCreate(BaseModel):
    """Схема создания вида деятельности."""

    name: str
    parent_id: int | None = None
    level: int = 1


class ActivityUpdate(BaseModel):
    """Схема обновления вида деятельности."""

    name: str | None = None
    parent_id: int | None = None
    level: int | None = None


class ActivityInDB(ActivityBase):
    """Схема вида деятельности в БД."""

    created_at: datetime
    updated_at: datetime


class ActivityResponse(ActivityBase):
    """Схема ответа для вида деятельности."""

    pass
