from __future__ import annotations
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from app.repos import EventRepository
from app.schemas import EventList, EventCreate, EventUpdate
from app.services.exceptions import EventNotFound

@dataclass(slots=True)
class EventService:
    session: AsyncSession

    @property
    def events(self) -> EventRepository:
        return EventRepository(self.session)

    async def create_event(self, event: EventCreate, cur_user_id: int) -> EventList:
        res = await self.events.create_event(**event.dict(), user_id=cur_user_id)
        await self.session.commit()
        await self.session.refresh(res)
        return res

    async def list_events(self) -> list[EventList]:
        event_list = await self.events.list_events()
        res = [EventList(**event.__dict__) for event in event_list]
        return res

    async def get_event(self, event_id: int) -> EventList:
        event = await self.events.get_event(event_id)
        if not event:
            raise EventNotFound()
        return EventList(**event.__dict__)
    
    async def update_event(self, event_id: int, payload: EventUpdate) -> EventList:
        event = await self.events.get_event(event_id)
        if not event:
            print("Event not found")
            raise EventNotFound()

        event = await self.events.update_event(event, payload)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def delete_event(self, event_id: int) -> None:
        event = await self.events.get_event(event_id)
        if not event:
            raise EventNotFound()
        await self.events.delete_event(event)
        await self.session.commit()

        
