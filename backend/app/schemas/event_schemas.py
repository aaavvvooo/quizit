from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    name: str
    starts_at: datetime
    venue: str
    price: Decimal
    image_url: str

class EventUpdate(BaseModel):
    name: str | None = None
    starts_at: datetime | None = None
    venue: str | None = None
    price: Decimal | None = None
    image_url: str | None = None

class EventList(BaseModel):
    id: int
    name: str
    starts_at: datetime = Field(validation_alias="starting_time")
    venue: str
    price: Decimal
    image_url: str
    status: str
    created_by: int

    model_config = {"from_attributes": True}
