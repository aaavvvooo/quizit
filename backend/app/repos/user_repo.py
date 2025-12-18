from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def get_user_by_id(self, user_id: int)-> User | None:
        res = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return res.scalar_one_or_none()

    async def get_user_by_email(self, email:str)-> User | None:
        res = await self.session.execute(
            select(User).where(User.email == email)
        ) 
        return res.scalar_one_or_none()
    
   
    async def create(self, name: str, email: str, hashed_password: str) -> User:
        user = User(name=name, email=email.lower(), hashed_password=hashed_password, is_active=True)
        self.session.add(user)
        await self.session.flush()  # gets PK without committing
        return user
