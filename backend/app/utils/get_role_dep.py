from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Role
from app.repos import RoleRepository
from app.utils.get_current_user_dep import get_current_user


async def get_role(
    session: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user),
) -> Role | None:
    repo = RoleRepository(session)
    return await repo.get_role(user_id)
