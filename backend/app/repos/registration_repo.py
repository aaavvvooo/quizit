from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EventRegistration, RegistrationType


class RegistrationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def has_registration(self, event_id: int, user_id: int) -> bool:
        res = await self.session.execute(
            select(EventRegistration.id).where(
                EventRegistration.event_id == event_id,
                EventRegistration.registered_by_user_id == user_id,
            )
        )
        return res.scalar_one_or_none() is not None

    async def create_registration(
        self,
        *,
        event_id: int,
        user_id: int,
        reg_type: RegistrationType,
        team_name: str | None,
        email: str,
        phone: str,
    ) -> EventRegistration:
        registration = EventRegistration(
            event_id=event_id,
            registered_by_user_id=user_id,
            type=reg_type,
            team_name=team_name,
            contact_email=email,
            contact_phone=phone,
        )
        self.session.add(registration)
        await self.session.flush()
        return registration

    async def list_for_event(self, event_id: int) -> list[EventRegistration]:
        res = await self.session.execute(
            select(EventRegistration).where(EventRegistration.event_id == event_id)
        )
        return res.scalars().all()
