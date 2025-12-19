from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services import EventService
from app.schemas import EventCreate, EventUpdate, EventList
from app.utils import get_current_user

router = APIRouter(prefix="/events", tags=["events"])

@router.post("", response_model=EventList, status_code=status.HTTP_201_CREATED)
async def create_event(
    payload: EventCreate, 
    session: AsyncSession = Depends(get_db),
    cur_user_id: int = Depends(get_current_user)    
):
    service = EventService(session)
    try:
        event = await service.create_event(payload, cur_user_id)
        return event
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong during event creation.")
