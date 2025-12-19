from __future__ import annotations
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from app.repos import EventRepository
from app.schemas import EventList, EventCreate

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
