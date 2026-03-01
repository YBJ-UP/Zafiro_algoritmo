from datetime import date, datetime
from model.calendar import agenda, actividades_response

# aqui son las funcionalidades pero ahorita

hola:agenda = {
    "id":"kamlkmlkamskmalk",
    "status":"tentative",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"eso tilin",
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "eventType":"default",
    "extras": { "etiquetas":[{"etiqueta":"chamba", "color":"#000000"}], "prioridad":"alta" }
}
adios:agenda = {
    "id":"fwfwfsscd",
    "status":"tentative",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"noc",
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "eventType":"default",
    "extras": { "etiquetas":[{"etiqueta":"chamba", "color":"#000000"}], "prioridad":"alta" }
}

njkadaskd:agenda = {
    "id":"jdsdnjas",
    "status":"tentative",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"sepa esto es d prueba",
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "eventType":"default",
    "extras": { "etiquetas":[{"etiqueta":"chamba", "color":"#000000"}], "prioridad":"alta" }
}

todo:actividades_response = { "defaultReminders":[{ "method":"email", "minutes":2 }], "items": [ hola, adios, njkadaskd ] }

print(todo)