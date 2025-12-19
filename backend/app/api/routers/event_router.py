from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services.event_service import EventService
from app.schemas import EventCreate, EventUpdate, EventList
from app.services.exceptions import EventNotFound
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

@router.get("", response_model=list[EventList])
async def get_events(
    session: AsyncSession = Depends(get_db),
    cur_user_id: int = Depends(get_current_user)
):
    service = EventService(session)
    try:
        events = await service.list_events()
        return events
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong during events listing.")

@router.get("/{event_id}", response_model=EventList)
async def get_event(
    sessiom: AsyncSession = Depends(get_db),
    cur_user_id: int = Depends(get_current_user),
    event_id: int = None
):
    service = EventService(sessiom)
    try:
        event = await service.get_event(event_id)
        return event
    except EventNotFound:
        raise HTTPException(status_code=404, detail="Event not found.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong during event retrieval.")

@router.patch("/{event_id}", response_model=EventList)
async def update_event(
    payload: EventUpdate,
    sessiom: AsyncSession = Depends(get_db),
    cur_user_id: int = Depends(get_current_user),
    event_id: int = None
):
    service = EventService(sessiom)
    try:
        event = await service.update_event(event_id, payload)
        return event
    except EventNotFound:
        raise HTTPException(status_code=404, detail="Event not found.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong during event update.")


@router.delete("/{event_id}")
async def delete_event(
    session: AsyncSession = Depends(get_db),
    cur_user_id: int = Depends(get_current_user),
    event_id: int = None
):
    service = EventService(session)
    try:
        await service.delete_event(event_id)
        return {"status": f"Event #{event_id} deleted successfully."}
    except EventNotFound:
        raise HTTPException(status_code=404, detail="Event not found.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong during event deletion.")


