from fastapi import APIRouter, Depends, HTTPException, Request, status
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List
from sqlmodel import select

event_router = APIRouter(
    tags=["Events"]
)

events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events

# $ curl localhost:8000/event/

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

# $ curl localhost:8000/event/1

@event_router.post("/new")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {
        "message": "Event created successfully."
    }

# $ curl -X POST localhost:8000/event/new -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"id": 1, "title": "FastAPI Book Launch", "image": "fastapi-book.jpeg", "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!", "tags": ["Python", "fastapi", "book", "launch"], "location": "Google Meet"}'

@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)

    if event:
        session.delete(event)
        session.commit()
        return {
            "message": "Event deleted successfully."
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Events with supplied ID does not exist"
    )

# $ curl -X DELETE localhost:8000/event/1

@event_router.delete("/")
async def delete_all_events(session=Depends(get_session)) -> dict:
    statement = select(Event)
    events = session.exec(statement).all()
    
    if events:
        for event in events:
            session.delete(event)
        session.commit()
        return {
            "message": "Event deleted successfully."
        }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No events found to delete"
    )

# $ curl -X DELETE localhost:8000/event/

@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)

        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

# $ curl -X PUT localhost:8000/event/edit/1 -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"title": "Packts FastAPI book launch II"}'