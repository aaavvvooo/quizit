from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional



class EventCreate(BaseModel):
    name: str
    starts_at: datetime
    venue: str  
    price: Decimal
    image_url: str

class EventUpdate(BaseModel):
    name: Optional[str] = None
    starts_at: Optional[datetime] = None
    venue: Optional[str] = None
    price: Optional[Decimal] = None
    image_url: Optional[str] = None

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
