from fastapi import APIRouter, Depends, HTTPException, Request, status
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(
    tags=["Events"]
)

events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

# $ curl localhost:8000/event/

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
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
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {
                "message": "Event deleted successfully."
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Events with supplied ID does not exist"
    )

# $ curl -X DELETE localhost:8000/event/1

@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message": "Events deleted successfully."
    }

# $ curl -X DELETE localhost:8000/event/