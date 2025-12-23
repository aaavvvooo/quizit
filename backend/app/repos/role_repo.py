from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Role, UserRole


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def has_role(self, user_id: int, role: str) -> bool:
        try:
            role_value = Role(role)
        except ValueError:
            return False

        res = await self.session.execute(
            select(UserRole.id).where(
                UserRole.user_id == user_id,
                UserRole.role == role_value,
            )
        )
        return res.scalar_one_or_none() is not None

    async def get_role(self, user_id: int) -> Role | None:
        res = await self.session.execute(
            select(UserRole.role).where(UserRole.user_id == user_id)
        )
        return res.scalars().first()
