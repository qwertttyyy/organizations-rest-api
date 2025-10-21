from datetime import datetime
from typing import Sequence

from pydantic import BaseModel, field_validator, constr

from .activity import ActivityResponse
from .building import BuildingResponse

PhoneStr = constr(pattern=r"^\+?[0-9()\-\s]{5,20}$")


class OrganizationBase(BaseModel):
    """Базовые поля организации."""

    id: int
    name: str
    building_id: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Проверяет длину названия."""
        if not 1 <= len(v) <= 255:
            raise ValueError("Имя должно содержать от 1 до 255 символов")
        return v


class OrganizationCreate(BaseModel):
    """Схема создания организации."""

    name: str
    building_id: int
    phones: list[PhoneStr] = []
    activity_ids: list[int] = []

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Проверяет длину названия."""
        if not 1 <= len(v) <= 255:
            raise ValueError("Имя должно содержать от 1 до 255 символов")
        return v

    @field_validator("phones")
    @classmethod
    def validate_phones_count(cls, v: list[PhoneStr]) -> list[PhoneStr]:
        """Ограничивает количество телефонов."""
        if len(v) > 10:
            raise ValueError("Organization can have at most 10 phone numbers")
        return v


class OrganizationUpdate(BaseModel):
    """Схема обновления организации."""

    name: str | None = None
    building_id: int | None = None
    phones: list[PhoneStr] | None = None
    activity_ids: list[int] | None = None


class OrganizationInDB(OrganizationBase):
    """Схема организации в БД."""

    created_at: datetime
    updated_at: datetime


class OrganizationResponse(BaseModel):
    """Схема ответа для организации."""

    id: int
    name: str
    building: BuildingResponse
    phones: list[str]
    activities: Sequence[ActivityResponse]
