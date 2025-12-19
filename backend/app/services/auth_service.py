from __future__ import annotations
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.jwt import create_access_token
from app.security.passwords import hash_password, verify_password, needs_rehash
from app.repos import AuthRepository
from app.services.exceptions import EmailAlreadyRegistered, InvalidCredentials


@dataclass(slots=True)
class AuthService:
    session: AsyncSession

    @property
    def users(self) -> AuthRepository:
        return AuthRepository(self.session)

    async def register(self, name: str,  email: str, password: str):
        existing = await self.users.get_user_by_email(email)
        if existing:
            raise EmailAlreadyRegistered()

        user = await self.users.create(name=name, email=email, hashed_password=hash_password(password))
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def login(self, username: str, password: str) -> str:
        user = await self.users.get_user_by_email(username)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentials()

        if needs_rehash(user.hashed_password):
            user.hashed_password = hash_password(password)
            await self.session.commit()

        return create_access_token(sub=str(user.id))
