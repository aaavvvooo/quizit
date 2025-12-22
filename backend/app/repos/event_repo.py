from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.models import EventStatus
from decimal import Decimal

from app.models import Event, EventStatus
from app.schemas import EventUpdate
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

    async def list_events(self) -> list[Event]:
        res = await self.session.execute(select(Event))
        return res.scalars().all()

    async def get_event(self, event_id: int) -> Event:
        res = await self.session.get(Event, event_id)
        return res

    async def update_event(self, event: Event, payload: EventUpdate) -> Event:
        update_data = payload.dict(exclude_unset=True, exclude_none=True)
        if "starts_at" in update_data:
            update_data["starting_time"] = update_data.pop("starts_at")

        for key, value in update_data.items():
            setattr(event, key, value)

        await self.session.flush()
        return event

    async def delete_event(self, event: Event) -> None:
        await self.session.delete(event)
        await self.session.flush()

    async def publish_event(self, event: Event, published_at: datetime) -> Event:
        event.status = EventStatus.UPCOMING
        event.published_at = published_at
        await self.session.flush()
        return event

    async def unpublish_event(self, event: Event) -> Event:
        event.status = EventStatus.DRAFT
        event.published_at = None
        await self.session.flush()
        return event

    async def start_event(self, event: Event, started_at: datetime) -> Event:
        event.status = EventStatus.ACTIVE
        event.started_at = started_at
        await self.session.flush()
        return event

    async def finish_event(self, event: Event, finished_at: datetime) -> Event:
        event.status = EventStatus.FINISHED
        event.finished_at = finished_at
        await self.session.flush()
        return event
