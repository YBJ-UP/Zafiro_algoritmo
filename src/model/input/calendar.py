from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

@dataclass
class creator:
    email:str
    self:bool

@dataclass
class start:
    date:date

@dataclass
class end:
    date:date



@dataclass
class agenda:
    kind:str
    etag:str
    id:str
    status: Literal["confirmed","tentative","cancelled"]
    htmlLink:str
    created:datetime
    updated:datetime
    summary:str
    creator: creator
    start:start
    end:end
    transparency:Literal["transparent","opaque"]
    iCalUID:str
    sequence:int
    reminders:bool
    eventType:Literal["default","birthday","focusTime","fromGmail","outOfOffice","workingLocation"]