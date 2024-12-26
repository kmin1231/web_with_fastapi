from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello, world!"
    }

# $ uvicorn api:app --port 8000 --reload
# $ curl http://localhost:8000