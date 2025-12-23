from enum import Enum
from typing import Optional
from decimal import Decimal
from datetime import datetime
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Role(str, Enum):
    ADMIN = "ADMIN"


class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[Role] = mapped_column(
        SAEnum(
            Role,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            name="role",
        ),
        default=Role.ADMIN,
        server_default=Role.ADMIN.value,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )