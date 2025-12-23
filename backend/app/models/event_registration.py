from __future__ import annotations

from enum import Enum
from datetime import datetime
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RegistrationType(str, Enum):
    USER = "USER"
    TEAM = "TEAM"


class EventRegistration(Base):
    __tablename__ = "event_registrations"
    __table_args__ = (
        UniqueConstraint("event_id", "registered_by_user_id", name="uq_event_registrations_event_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    registered_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[RegistrationType] = mapped_column(
        SAEnum(
            RegistrationType,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            name="registration_type",
            create_type=False,
        ),
        nullable=False,
    )
    team_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[str] = mapped_column(String(320), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
