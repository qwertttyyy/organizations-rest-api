from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime, Numeric

from . import Base

if TYPE_CHECKING:
    from .organization import Organization  # pragma: no cover


class Building(Base):
    """Здание.

    Attributes:
        id: Идентификатор.
        address: Уникальный адрес здания.
        latitude: Широта с точностью до 7 знаков.
        longitude: Долгота с точностью до 7 знаков.
        created_at: Дата создания.
        updated_at: Дата обновления.
        organizations: Связанные организации.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    latitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 7), nullable=False, index=True
    )
    longitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 7), nullable=False, index=True
    )
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="building", cascade="save-update", passive_deletes="all"
    )

    __table_args__ = (
        UniqueConstraint("address", name="uq_building_address"),
        Index("ix_building_lat_lon", "latitude", "longitude"),
    )
