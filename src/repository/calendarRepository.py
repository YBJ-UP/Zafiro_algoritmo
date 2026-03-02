from datetime import date, datetime
from model.calendar import agenda, actividades_response

# aqui son las funcionalidades pero ahorita

# PSEUDOCODIGO

# INICIO

# RECIBIR actividades
# RECIBIR restricciones
#   RECIBIR gap (espacio entre actividades)
#   RECIBIR tag (¿se le dará prioridad a cierto tipo de actividades según sus etiquetas?)
#   RECIBIR ??? (noc q más llevaría)

# ANALIZAR actividades
#   SI start.timezone NO EXISTE ENTONCES es estática Y NO se pueden poner actividades en ese dia
#   SI transparency ES IGUAL A opaque ENTONCES es estática
#   REORDENAR POR extras.prioridad DE alta A baja
#   REORDENAR POR extras.etiquetas PRIMERO tag

# 

# FIN

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
    "extras": { "etiquetas":[{"etiqueta":"chamba", "color":"#ff0000"}], "prioridad":"alta" }
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
    "extras": { "etiquetas":[{"etiqueta":"estudio", "color":"#00ff00"}], "prioridad":"alta" }
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
    "extras": { "etiquetas":[{"etiqueta":"personal", "color":"#0000ff"}], "prioridad":"alta" }
}

todo:actividades_response = { "defaultReminders":[{ "method":"email", "minutes":2 }], "items": [ hola, adios, njkadaskd ] }

print(todo)