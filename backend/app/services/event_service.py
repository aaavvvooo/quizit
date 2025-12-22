from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.repos import EventRepository
from app.schemas import EventList, EventCreate, EventUpdate
from app.models import EventStatus
from app.services.exceptions import EventNotFound, EventInvalidStatus

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

    async def transition_event_status(self, event_id: int, target: EventStatus) -> None:
        event = await self.events.get_event(event_id)
        if not event:
            raise EventNotFound()

        now = datetime.now(timezone.utc)
        transitions = {
            EventStatus.UPCOMING: {
                "allowed": {EventStatus.DRAFT},
                "apply": lambda: self.events.publish_event(event, now),
                "error": "Event must be in draft to publish.",
            },
            EventStatus.DRAFT: {
                "allowed": {EventStatus.UPCOMING},
                "apply": lambda: self.events.unpublish_event(event),
                "error": "Event must be upcoming to unpublish.",
            },
            EventStatus.ACTIVE: {
                "allowed": {EventStatus.UPCOMING},
                "apply": lambda: self.events.start_event(event, now),
                "error": "Event must be upcoming to start.",
            },
            EventStatus.FINISHED: {
                "allowed": {EventStatus.ACTIVE},
                "apply": lambda: self.events.finish_event(event, now),
                "error": "Event must be active to finish.",
            },
        }

        transition = transitions.get(target)
        if not transition:
            raise EventInvalidStatus("Unsupported status transition.")
        if event.status not in transition["allowed"]:
            raise EventInvalidStatus(transition["error"])

        await transition["apply"]()
        await self.session.commit()

    async def publish_event(self, event_id: int) -> None:
        await self.transition_event_status(event_id, EventStatus.UPCOMING)

    async def unpublish_event(self, event_id: int) -> None:
        await self.transition_event_status(event_id, EventStatus.DRAFT)

    async def start_event(self, event_id: int) -> None:
        await self.transition_event_status(event_id, EventStatus.ACTIVE)

    async def finish_event(self, event_id: int) -> None:
        await self.transition_event_status(event_id, EventStatus.FINISHED)
        
