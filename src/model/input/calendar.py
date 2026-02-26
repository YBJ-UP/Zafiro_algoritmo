from datetime import date, datetime
from typing import Literal, NotRequired, TypedDict

class creator_dict(TypedDict):
    email:str
    self:NotRequired[bool]

class date_dict(TypedDict):
    date:NotRequired[str]
    dateTime:NotRequired[str]
    timeZone:NotRequired[str]

class reminder_override(TypedDict):
    method:Literal["email","popup"]
    minutes:int

class reminder_dict(TypedDict):
    useDefault:bool
    overrides:NotRequired[list[reminder_override]]

class extras_dict(TypedDict):
    prioridad: Literal["baja","media","alta"]
    etiquetas: list[str]

class agenda(TypedDict):
    kind:str
    etag:str
    id:str
    status: Literal["confirmed","tentative","cancelled"]
    htmlLink:str
    created:str
    updated:str
    summary:NotRequired[str]
    creator:creator_dict
    organizer:creator_dict
    start:date_dict
    end:date_dict

    # solo en cosas q c repiten
    recurringEventId:NotRequired[str]
    originalStartTime:NotRequired[date_dict]

    transparency:NotRequired[Literal["transparent","opaque"]]
    iCalUID:str
    sequence:int
    reminders:reminder_dict
    eventType:Literal["default","birthday","focusTime","fromGmail","outOfOffice","workingLocation"]

hola:agenda = {
    "kind":"aaa",
    "etag":"dddddd",
    "id":"kamlkmlkamskmalk",
    "status":"tentative",
    "htmlLink":"lksklmdslk",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"eso tilin",
    "creator": { "email":"correo", "self":False },
    "organizer": { "email":"safaf", "self":False },
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "iCalUID":"kasmslkmafmakf",
    "sequence":0,
    "reminders": { "useDefault":True },
    "eventType":"default"
}

print(hola)