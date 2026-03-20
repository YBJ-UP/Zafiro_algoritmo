from typing import Literal
from pydantic import BaseModel

# -------------------------------------------------------------------------------

class DateDict(BaseModel):
    date:str | None = None
    dateTime:str | None = None
    timeZone:str | None = None

# -------------------------------------------------------------------------------

class ReminderOverride(BaseModel):
    method:Literal["popup"]
    minutes:int

# -------------------------------------------------------------------------------

class ReminderDict(BaseModel):
    useDefault:bool
    overrides:list[ReminderOverride] | None = None

# -------------------------------------------------------------------------------

class etiquetas_dict(BaseModel):
    etiqueta:str
    color:str

# -------------------------------------------------------------------------------

class ExtrasDict(BaseModel):
    prioridad: Literal["baja","media","alta"]
    etiquetas: etiquetas_dict

# -------------------------------------------------------------------------------

class Agenda(BaseModel):
    id:str
    created:str
    updated:str
    summary:str
    start:DateDict
    end:DateDict

    # solo en cosas q c repiten
    recurringEventId:str | None = None
    originalStartTime:DateDict | None = None

    transparency:Literal["transparent","opaque"]
    reminders:ReminderDict

    extras:ExtrasDict

# -------------------------------------------------------------------------------

class ActividadesResponse(BaseModel): # tiene mas atributos pero estos son los q realmente importan
    defaultReminders:list[ReminderOverride]
    items: list[Agenda]

# -------------------------------------------------------------------------------