from datetime import date, datetime
from typing import Literal, NotRequired, TypedDict

class creator_dict(TypedDict):
    email:str
    self:NotRequired[bool]

# -------------------------------------------------------------------------------

class date_dict(TypedDict):
    date:NotRequired[str]
    dateTime:NotRequired[str]
    timeZone:NotRequired[str]

# -------------------------------------------------------------------------------

class reminder_override(TypedDict):
    method:Literal["email","popup"]
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

class agenda_processed(TypedDict):
    id:str
    status: Literal["confirmed","tentative","cancelled"]
    created:str
    updated:str
    summary:NotRequired[str]
    organizer:creator_dict
    start:date_dict
    end:date_dict

    # solo en cosas q c repiten
    recurringEventId:NotRequired[str]
    originalStartTime:NotRequired[date_dict]

    transparency:NotRequired[Literal["transparent","opaque"]]
    reminders:reminder_dict
    eventType:Literal["default","birthday","focusTime","fromGmail","outOfOffice","workingLocation"]

    extras:extras_dict

# -------------------------------------------------------------------------------

class actividades_response_processed(TypedDict): # tiene mas atributos pero estos son los q realmente importan
    defaultReminders:list[reminder_override]
    items: list[agenda_processed]

# -------------------------------------------------------------------------------

hola:agenda_processed = {
    "id":"kamlkmlkamskmalk",
    "status":"tentative",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"eso tilin",
    "organizer": { "email":"safaf", "self":False },
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "eventType":"default",
    "extras": { "etiquetas":[{"etiqueta":"chamba", "color":"#000000"}], "prioridad":"alta" }
}
adios:agenda_processed = {
    "id":"fwfwfsscd",
    "status":"tentative",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"noc",
    "organizer": { "email":"safaf", "self":False },
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "eventType":"default",
    "extras": { "etiquetas":[{"etiqueta":"chamba", "color":"#000000"}], "prioridad":"alta" }
}

njkadaskd:agenda_processed = {
    "id":"jdsdnjas",
    "status":"tentative",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"sepa esto es d prueba",
    "organizer": { "email":"safaf", "self":False },
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "eventType":"default",
    "extras": { "etiquetas":[{"etiqueta":"chamba", "color":"#000000"}], "prioridad":"alta" }
}

todo:actividades_response_processed = { "defaultReminders":[{ "method":"email", "minutes":2 }], "items": [ hola, adios, njkadaskd ] }

print(todo)