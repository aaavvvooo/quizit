from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user_schemas import UserCreate, UserPublic, TokenResponse, UserLogin, GoogleAuthRequest
from app.security.jwt import decode_token, TokenError
from app.services.auth_service import AuthService
from app.services.exceptions import EmailAlreadyRegistered, InvalidCredentials, InvalidGoogleToken

from app.models import User
from app.utils import get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_db)):
    service = AuthService(session)
    try:
        user = await service.register(
            name=payload.name,
            email=str(payload.email).lower(),
            password=payload.password,
        )
        return user
    except EmailAlreadyRegistered:
        raise HTTPException(status_code=400, detail="Email already registered")

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(session)
    try:
        tokens = await auth_service.login(username=payload.email, password=payload.password)
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return TokenResponse(access_token=tokens) 


@router.post("/token", response_model=TokenResponse)
async def token(form: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(session)
    token = await auth_service.login(username=form.username, password=form.password)
    return TokenResponse(access_token=token)


@router.post("/google", response_model=TokenResponse)
async def google_auth(payload: GoogleAuthRequest, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(session)
    try:
        token = await auth_service.login_with_google(payload.id_token)
    except InvalidGoogleToken:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    return TokenResponse(access_token=token)


@router.get("/me")
async def me(user_id: int = Depends(require_role("ADMIN"))):
    return {"user_id": user_id}
