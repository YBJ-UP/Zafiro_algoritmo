from datetime import date, datetime
from model.calendar import agenda, actividades_response

# aqui son las funcionalidades pero ahorita

# PSEUDOCODIGO

# INICIO

# RECIBIR actividades
# RECIBIR restricciones
#   tiempo de descanso
#   gap? //espacio entre actividades
#   tag? //¿se le dará prioridad a cierto tipo de actividades según sus etiquetas? ¿no será mucho poner esto?
#   ??? //noc q más llevaría

# ANALIZAR actividades
#   SI actividad.start.timezone NO EXISTE ENTONCES es estática Y NO se pueden poner actividades en ese dia //por si alguna tarea se tiene que mover de día
#   SI actividad.transparency ES IGUAL A opaque ENTONCES es estática
#   CALCULAR duración de cada actividad //algún método ha de haber para restar fechas COMO actividad.duracion //se le añadiría este atributo
#   REORDENAR POR extras.prioridad DE alta A baja //creo que se habían sacado de extras pero no recuerdo
#   SI tag EXISTE REORDENAR POR extras.etiquetas PRIMERO tag

# DEFINIR dias_inhabiles SEGÚN actividad DONDE actividad.start.timeZone NO EXISTE
# //quedaria algo como dias_inhabiles = [{"2026-03-13"},{"2026-03-14"}..] o al menos eso pienso

# DEFINIR rangos_utilizables SEGÚN tiempo de descanso Y actividades opacas
# //aunque en teoría el tiempo de descanso se guarda como una actividad opaca así q noc
# //según yo quedaría algo como rango_utilizable = [{7,8},{17,19},{21,22}] pero no sé cómo sería así de 7:30 u horas no exactas
# //otra cosa es que así el espacio entre cada una se tiene que calcular al momento y no sé qué tan bueno sea eso
# //la verdad no creo que eso sea tan problemático así que equis

# //por ahora asumiré q la duración ya viene dentro del rango, algo como { inicio=fecha1, fin=fecha2, duracion=numero } aunque lo veo algo noc, igual guardar con fecha hace que no se ponga el dia por aparte
# //puede que la duración se guarde en segundos para no andar quemandome tanto el coco

# //ORGANIZAR
# ITERAR EN rango_utilizable COMO i //no tocará los días inhabiles, creo que no es necesario definirlos
#   POR actividad DE actividades //ya vienen ordenadas por prioridad y etiqueta si esta se especificó
#       SI actividad.duracion ES MAYOR A rango_utilizable[i].duracion ENTONCES SALTAR
#       ASIGNAR rango_utilizable[i].inicio A actividad.start.dateTime
#       CALCULAR fecha en la que acaba COMO actividad.end.dateTime
#       SIGUIENTE i //así como lo veo no tiene backtracking
# //creo que las iteraciones están al revés, debería iterar primero por actividad y después por el otro
# //aún falta pero bueno

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