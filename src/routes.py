from typing import Annotated

from fastapi import FastAPI, HTTPException, Header
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
def sort_calendar(payload: Annotated[str | None, Header()] = None) -> str:
    if payload is not None:
        decoded_payload = jwt.decode(jwt=payload, key=key, algorithms=["HS256"])
        data = CalendarResponse(**decoded_payload)
        response = sortCalendarController(data=data)
        return jwt.encode(payload=response, key=key, algorithm="HS256" )
    else:
        raise HTTPException(status_code=400, detail="No se enviaron datos")