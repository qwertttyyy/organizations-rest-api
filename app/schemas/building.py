from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator


class BuildingBase(BaseModel):
    """Базовые поля здания."""

    id: int
    address: str
    latitude: Decimal
    longitude: Decimal

    @field_validator("latitude")
    @classmethod
    def validate_lat(cls, v: Decimal) -> Decimal:
        """Проверяет диапазон широты."""
        if v < Decimal("-90") or v > Decimal("90"):
            raise ValueError("Широта должна быть в диапазоне от -90 до 90")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_lon(cls, v: Decimal) -> Decimal:
        """Проверяет диапазон долготы."""
        if v < Decimal("-180") or v > Decimal("180"):
            raise ValueError(
                "Долгота должна находиться в диапазоне от -180 до 180"
            )
        return v


class BuildingCreate(BaseModel):
    """Схема создания здания."""

    address: str
    latitude: Decimal
    longitude: Decimal


class BuildingUpdate(BaseModel):
    """Схема обновления здания."""

    address: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class BuildingInDB(BuildingBase):
    """Схема здания в БД."""

    created_at: datetime
    updated_at: datetime


class BuildingResponse(BuildingBase):
    """Схема ответа для здания."""

    pass
