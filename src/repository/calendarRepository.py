from datetime import date, datetime
from model.calendar import agenda, actividades_response

# aqui son las funcionalidades pero ahorita

# PSEUDOCODIGO

# //metaheuristica

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
#   SI tag EXISTE REORDENAR actividades SEGUN extras.tag, extras.prioridad SI NO REORDENAR actividades SEGUN extras.prioridad FIN SI

# DEFINIR dias_inhabiles SEGÚN actividad DONDE actividad.transparency IGUAL A opaque
# //quedaria algo como dias_inhabiles = [{"2026-03-13"},{"2026-03-14"}..] o al menos eso pienso
# //viendolo bn noc pq tiene corchetes

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
# //no recalcula el tiempo disponible

# //va de nuez pq no quiero borrar todo, el bloque anterior hagan d cuenta q no existe
# POR actividad DE actividades
#   ITERAR EN rango_utilizable COMO i
#       SI actividad.duracion MAYOR A rango_utilizable[i].duracion ENTONCES SALTAR FIN SI
#       ASIGNAR rango_utilizable[i].inicio A actividad.start.dateTime
#       CALCULAR fecha en la que acaba COMO actividad.end.dateTime
#       CALCULAR actividad.duracion //de nuevo
#       SI actividad.duracion IGUAL A rango_utilizable[i].duracion ENTONCES rango_utilizable[i].pop() //o su equivalente en python
#       SI NO rango_utilizable[i].inicio = actividad.end.dateTime + gap FIN SI
#       SIGUIENTE i //así como lo veo no tiene backtracking

# //aún falta pero bueno

# FIN
# todo esto se descarta pq es una cochinada segun chat y todavia es voraz xd

# INICIO

# //será beam search pq no le entendi al otro y tardaria muchisimo mas d lo optimo

# INICIO FUNCION getTime( actividades, tiempo_descanso )

# DEFINIR tiempo_libre:{ inicio:fecha, fin:fecha }[] = [] //algo como { inicio:8:00, fin:9:30 }
# DEFINIR tiempo_ocupado:{ inicio:hora, fin:hora }[] = []

# tiempo_ocupado.append(tiempo_descanso) //lo mejor sería que el tiempo de descanso ya tuviese la misma forma

# POR CADA actividad DE actividades
#   SI actividad.transparency IGUAL A opaque ENTONCES
#       tiempo_ocupado.append({ inicio:actividad.start.dateTime, fin:actividad.end.dateTime }) //si es solo date, creo que se tapa el día entero
#       //algo para obtener el tiempo libre, la verdad no sé muy bien cómo hacerlo
#   FIN SI

# RETORNAR { tiempo_libre, tiempo_ocupado }

# FIN FUNCION getTime

# INICIO MAIN( actividades, tiempo_descanso, gap=15, tag?, tag_restriction?, long_first=falso )
#   //tiempo_descanso: algo como { inicio:20:00, fin:6:15 }
#   //gap: espacio entre actividades, predeterminado 10
#   //tag?: ¿se le dará prioridad a cierto tipo de actividades según sus etiquetas?
#   //tag_restriction?: ¿se pueden restringir ciertas etiquetas a ciertos horarios? tal vez se añada después
#   //long_first: predeterminado falso, si las actividades largas deberian ir primero

# DEFINIR ancho_haz COMO {valor arbitrario} //de preferencia un numero pequeño
# DEFINIR candidatos COMO lista[ {candidato:agenda[], puntaje:int} ] //el puntaje se calcula en otra funcion

# response IGUAL A REORDENAR actividades
#   SEGÚN tag SI EXISTE
#   SEGÚN prioridad
#   SEGÚN duracion SI long_first

# { tiempo_libre, tiempo_ocupado } = getTime( actividades, tiempo_descanso )

# FIN MAIN
# FIN

hola:agenda = {
    "id":"kamlkmlkamskmalk",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"eso tilin",
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":[{"etiqueta":"chamba", "color":"#ff0000"}], "prioridad":"alta" }
}
adios:agenda = {
    "id":"fwfwfsscd",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"noc",
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":[{"etiqueta":"estudio", "color":"#00ff00"}], "prioridad":"alta" }
}

njkadaskd:agenda = {
    "id":"jdsdnjas",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"sepa esto es d prueba",
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":[{"etiqueta":"personal", "color":"#0000ff"}], "prioridad":"alta" }
}

todo:actividades_response = { "defaultReminders":[{ "method":"popup", "minutes":2 }], "items": [ hola, adios, njkadaskd ] }

print(todo)