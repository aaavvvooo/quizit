from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from decimal import Decimal

from app.models import Event
class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_event(
        self,
        name: str,
        starts_at: datetime,
        venue: str,
        price: Decimal,
        image_url: str,
        user_id: int,
    ) -> Event:
        event = Event(
            name=name,
            starting_time=starts_at,
            venue=venue,
            price=price,
            image_url=image_url,
            created_by=user_id,
        )
        self.session.add(event)
        await self.session.flush()
        return event
