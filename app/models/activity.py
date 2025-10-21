from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, CheckConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from . import Base

if TYPE_CHECKING:
    from .organization import Organization  # pragma: no cover


class Activity(Base):
    """Вид деятельности с иерархией до 3 уровней.

    Attributes:
        id: Идентификатор.
        name: Название.
        parent_id: Родительский вид деятельности.
        level: Уровень вложенности от 1 до 3.
        created_at: Дата создания.
        updated_at: Дата обновления.
        parent: Родитель.
        children: Список дочерних видов.
        organizations: Организации, связанные через M2M.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activity.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    level: Mapped[int] = mapped_column(nullable=False, default=1)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    parent: Mapped["Activity | None"] = relationship(
        remote_side="Activity.id", back_populates="children"
    )
    children: Mapped[list["Activity"]] = relationship(
        back_populates="parent", cascade="save-update"
    )

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities",
    )

    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="level_between_1_3"),
        Index("ix_activity_parent_id", "parent_id"),
    )
