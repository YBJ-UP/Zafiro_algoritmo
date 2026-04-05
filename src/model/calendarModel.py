from datetime import datetime
from typing import Literal, TypedDict
from pydantic import BaseModel

# -------------------------------------------------------------------------------

class DateDict(BaseModel):
    date:str | None = None
    dateTime:str | None = None
    timeZone:str | None = None

# -------------------------------------------------------------------------------

class ReminderOverride(BaseModel):
    method:Literal["popup", "email"]
    minutes:int

# -------------------------------------------------------------------------------

class ReminderDict(BaseModel):
    useDefault:bool
    overrides:list[ReminderOverride] | None = None

# -------------------------------------------------------------------------------

class EtiquetasDict(BaseModel):
    etiqueta:int
    color:str

# -------------------------------------------------------------------------------

class ExtrasDict(BaseModel):
    prioridad: Literal["baja","media","alta"]
    etiquetas: EtiquetasDict

# -------------------------------------------------------------------------------

class Agenda(BaseModel):
    id:str
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

class RangoTiempo(TypedDict):
    inicio:str
    fin:str

# -------------------------------------------------------------------------------

class RangoTiempoDt(TypedDict):
    inicio:datetime
    fin:datetime

# -------------------------------------------------------------------------------

class Candidato:
    tareas_agendadas:list[Agenda]
    tareas_no_agendadas:list[Agenda]
    tiempo_libre_restante:list[RangoTiempoDt]
    puntaje:float

    def __init__(self) -> None:
        self.tareas_agendadas = []
        self.tareas_no_agendadas = []
        self.tiempo_libre_restante = []
        self.puntaje = 0.0
