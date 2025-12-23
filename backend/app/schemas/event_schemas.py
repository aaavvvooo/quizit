from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from app.models import RegistrationType


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


class EventRegistrationCreate(BaseModel):
    type: RegistrationType
    email: EmailStr
    phone: str = Field(min_length=5, max_length=32)
    team_name: Optional[str] = None


class EventRegistrationList(BaseModel):
    id: int
    event_id: int
    registered_by_user_id: int
    type: RegistrationType
    team_name: Optional[str]
    email: EmailStr = Field(validation_alias="contact_email")
    phone: str = Field(validation_alias="contact_phone")
    created_at: datetime

    model_config = {"from_attributes": True}
