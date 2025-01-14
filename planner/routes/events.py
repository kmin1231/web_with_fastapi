from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends, status
from database.connection import Database
from auth.authenticate import authenticate

from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events

# $ curl localhost:8000/event/


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event

# $ curl localhost:8000/event/1


@event_router.post("/new")
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    await event_database.save(body)

    return {
        "message": "Event created successfully."
    }

# $ curl -X POST localhost:8000/event/new -H 'accept: application/json' -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=&username=reader%40packt.com&password=exemplary&scope=&client_id=&client_secret='

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_database.delete(id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Events with supplied ID does not exist"
        )
    
    return {
        "message": "Event deleted successfully."
    }

# $ curl -X DELETE localhost:8000/event/1


@event_router.delete("/")
async def delete_all_events() -> dict:
    events = await event_database.get_all()

    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No events found to delete"
        )

    for event in events:
        await event_database.delete(event.id)

    return {
        "message": "Event deleted successfully."
    }    

# $ curl -X DELETE localhost:8000/event/


@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate, user: str = Depends(authenticate)) -> Event:
    updated_event = await event_database.update(id, body)
    
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event

# $ curl -X PUT localhost:8000/event/edit/1 -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"title": "Packts FastAPI book launch II"}'