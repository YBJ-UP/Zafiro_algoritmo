from fastapi import FastAPI
from controller.calendarController import CalendarResponse, sortCalendarController

app = FastAPI()

@app.get("/api/health")
def health_check():
    return {"message": "hola.mundo(\"print;\")"}

@app.post("/api/sort")
def sort_calendar(data:CalendarResponse):
    return sortCalendarController(data=data)