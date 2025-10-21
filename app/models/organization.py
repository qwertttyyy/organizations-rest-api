from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    ForeignKey,
    Table,
    Column,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from . import Base

if TYPE_CHECKING:
    from .building import Building  # pragma: no cover
    from .activity import Activity  # pragma: no cover

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column(
        "organization_id",
        ForeignKey("organization.id", ondelete="RESTRICT"),
        primary_key=True,
    ),
    Column(
        "activity_id",
        ForeignKey("activity.id", ondelete="RESTRICT"),
        primary_key=True,
    ),
)


class Organization(Base):
    """Организация.

    Attributes:
        id: Идентификатор.
        name: Название.
        building_id: Идентификатор здания.
        created_at: Дата создания.
        updated_at: Дата обновления.
        building: Связанное здание.
        phones: Список телефонов.
        activities: Виды деятельности.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("building.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
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

    building: Mapped["Building"] = relationship(back_populates="organizations")
    phones: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary=organization_activities,
        back_populates="organizations",
    )


class OrganizationPhone(Base):
    """Телефон организации.

    Attributes:
        id: Идентификатор.
        organization_id: Идентификатор организации.
        phone_number: Уникальный номер телефона.
        organization: Обратная связь с организацией.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    phone_number: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True, index=True
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="phones"
    )

    __table_args__ = (
        UniqueConstraint("phone_number", name="uq_org_phone_phone_number"),
    )
