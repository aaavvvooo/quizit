from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repos import RoleRepository
from app.utils.get_current_user_dep import get_current_user


def require_role(role: str):
    async def _require_role(
        session: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user),
    ) -> int:
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized user",
            )

        repo = RoleRepository(session)
        has_role = await repo.has_role(user_id, role)
        if not has_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )
        return user_id

    return _require_role
