from fastapi import FastAPI
from dotenv import load_dotenv
from os import getenv
import jwt
from src.controller.calendarController import CalendarResponse, sortCalendarController

load_dotenv()
key: str | None = getenv("CLERK_SECRET_KEY")
assert key is not None
app = FastAPI()

@app.get(path="/api/health")
def health_check() -> dict[str, str]:
    return {"message": "hola.mundo(\"print;\")"}

@app.post(path="/api/sort")
def sort_calendar(data:CalendarResponse) -> str:
    response = sortCalendarController(data=data)
    return jwt.encode(payload=response, key=key, algorithm="HS256" )