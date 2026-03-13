from typing import Literal, NotRequired, TypedDict

# -------------------------------------------------------------------------------

class date_dict(TypedDict):
    date:NotRequired[str]
    dateTime:NotRequired[str]
    timeZone:NotRequired[str]

# -------------------------------------------------------------------------------

class reminder_override(TypedDict):
    method:Literal["popup"]
    minutes:int

# -------------------------------------------------------------------------------

class reminder_dict(TypedDict):
    useDefault:bool
    overrides:NotRequired[list[reminder_override]]

# -------------------------------------------------------------------------------

class etiquetas_dict(TypedDict):
    etiqueta:str
    color:str

# -------------------------------------------------------------------------------

class extras_dict(TypedDict):
    prioridad: Literal["baja","media","alta"]
    etiquetas: list[etiquetas_dict]

# -------------------------------------------------------------------------------

class agenda(TypedDict):
    id:str
    created:str
    updated:str
    summary:str
    start:date_dict
    end:date_dict

    # solo en cosas q c repiten
    recurringEventId:NotRequired[str]
    originalStartTime:NotRequired[date_dict]

    transparency:Literal["transparent","opaque"]
    reminders:reminder_dict

    extras:extras_dict

# -------------------------------------------------------------------------------

class actividades_response(TypedDict): # tiene mas atributos pero estos son los q realmente importan
    defaultReminders:list[reminder_override]
    items: list[agenda]

# -------------------------------------------------------------------------------