from __future__ import annotations
from dataclasses import dataclass
import secrets
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.jwt import create_access_token
from app.security.passwords import hash_password, verify_password, needs_rehash
from app.repos import AuthRepository
from app.services.exceptions import EmailAlreadyRegistered, InvalidCredentials, InvalidGoogleToken
from app.core.config import settings

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token


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

    async def login_with_google(self, id_token: str) -> str:
        if not settings.google_client_id:
            raise InvalidGoogleToken() 

        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token,
                google_requests.Request(),
                settings.google_client_id,
            )
        except ValueError as e:
            raise InvalidGoogleToken() from e

        email = idinfo.get("email")
        if not email:
            raise InvalidGoogleToken()

        user = await self.users.get_user_by_email(email.lower())
        if not user:
            display_name = idinfo.get("name") or idinfo.get("given_name") or ""
            random_password = secrets.token_urlsafe(32)
            user = await self.users.create(
                name=display_name,
                email=email.lower(),
                hashed_password=hash_password(random_password),
            )
            await self.session.commit()
            await self.session.refresh(user)

        return create_access_token(sub=str(user.id))
