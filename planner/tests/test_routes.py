import httpx
import pytest
from typing import AsyncGenerator

from planner.auth.jwt_handler import create_access_token
from planner.models.events import Event


@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("testuser@packt.com")

@pytest.fixture(scope="module")
async def mock_event() -> AsyncGenerator[Event, None]:
    new_event = Event(
        creator="testuser@packt.com",
        title="FastAPI Book Launch",
        image="https://linktomyimage.com/image.png",
        description="We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
        tags=["python", "fastapi", "book", "launch"],
        location="Google Meet"
    )

    await Event.insert_one(new_event)

    yield new_event


@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event")

    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)

@pytest.matk.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload = {
        "title": "FastAPI Book Launch",
        "image": "https://linktomyimage.com/image.png",
        "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
        "tags": ["python", "fastapi", "book", "launch"],
        "location": "Google Meet",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    test_response = {
        "message": "Event created successfully"
    }

    response = await default_client.post("/event/new", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response