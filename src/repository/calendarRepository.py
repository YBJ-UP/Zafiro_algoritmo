from datetime import date, datetime, time, timedelta
from typing import TypedDict
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.calendarModel import agenda, actividades_response

# aqui son las funcionalidades pero ahorita

# PSEUDOCODIGO

# //metaheuristica

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

# algun dia pondre estas en model pq ahi van

# DICCIONARIOS DE APOYO

class rango_tiempo(TypedDict):
    inicio:date
    fin:date

# -------------------------------------------------------------------------------

class rango_tiempo_dt(TypedDict):
    inicio:datetime
    fin:datetime

# -------------------------------------------------------------------------------

class restricciones_etiquetas(TypedDict):
    tag:str
    horario:rango_tiempo

# -------------------------------------------------------------------------------

class candidato:
    tareas_agendadas:list[agenda] = []
    tareas_no_agendadas:list[agenda] = []
    tiempo_libre_restante:list[rango_tiempo_dt] = []
    puntaje:int = 0

# FUNCIONES DE APOYO

def convertDate(fecha:str, tiempo:time) -> datetime:
    fecha_parsed = date.strptime( fecha, "%Y-%m-%d" )
    return datetime.combine(fecha_parsed, tiempo)

# -------------------------------------------------------------------------------

def convertStrToDt(fecha:str) -> datetime:
    return datetime.fromisoformat(fecha)

# -------------------------------------------------------------------------------

def orderByPriority(e:agenda):
    match e["extras"]["prioridad"]:
        case "alta":
            return 1
        case "media":
            return 2
        case "baja":
            return 3

# -------------------------------------------------------------------------------

def fuseTimes(tiempos:list[rango_tiempo_dt]) -> list[rango_tiempo_dt]:
    if not tiempos:
        return []
    tiempo_reordenado:list[rango_tiempo_dt] = sorted(tiempos, key=lambda e:e["inicio"])

    fusionados:list[rango_tiempo_dt] = [tiempo_reordenado[0]]

    for tarea in tiempo_reordenado[1:]:
        tarea_previa = fusionados[-1]
        if tarea["inicio"] <= tarea_previa["fin"]:
            tarea_previa["fin"] = max(tarea["fin"], tarea_previa["fin"])
        else:
            fusionados.append(tarea)
    return fusionados

# -------------------------------------------------------------------------------

def getFreeTime():
    print("aaa")

# FUNCIÓN PRINCIPAL

def sortCalendar(
        actividades:list[agenda],
        tiempo_descanso:rango_tiempo, # este se concertirá en un arreglo de dateTime
        dias_contemplados:int = 7, # hasta cuantos dias se puede recorrer una tarea supongo
        gap:int = 15,
        tag:str | None = None,
        tag_restriction:restricciones_etiquetas | None = None, #podria venir como un arreglo de restricciones pero por los tiempos capaz y ni siquiera se implemente
        long_first:bool = False
) -> None: #none por ahora
    ancho_haz = 5

    actividades_estaticas:list[agenda] = []
    actividades_libres:list[agenda] = []

    # tiempo_libre:list[rango_tiempo_dt] = [] # no sé como manejarlo, entiendo que lo mejor seria tenerlo pero que tal si se acomodan las tareas alrededor del tiempo ocupado
    tiempo_ocupado:list[rango_tiempo_dt] = []

    # para actividades que tomen todo el dia
    inicioDia:time = time(0,0,0)
    finDia:time = time(23,59,59)


    for actividad in actividades:
        if actividad["transparency"] == "opaque":
            if "date" in actividad["start"]:
                assert "date" in actividad["end"]
                tiempo_ocupado.append( { "inicio":convertDate( actividad["start"]["date"], inicioDia ), "fin":convertDate( actividad["end"]["date"], finDia ) } )
            else:
                assert "dateTime" in actividad["start"] and "dateTime" in actividad["end"]
                tiempo_ocupado.append({ "inicio":convertStrToDt(actividad["start"]["dateTime"]), "fin":convertStrToDt(actividad["end"]["dateTime"]) })
            actividades_estaticas.append(actividad)
        else:
            actividades_libres.append(actividad)
        
    actividades_libres.sort(key=orderByPriority)

    fecha_maxima = date.today() + timedelta(days=dias_contemplados)

    for i in range(dias_contemplados): # se suppone que con este se transforman en datetime los dias libres, podria ser una funcion de apoyo
        print(i)

    print(fecha_maxima) # el editor m da lata si no accedo a los datos
    print(ancho_haz)
    print(tiempo_ocupado)
    print(actividades_libres)



hola:agenda = {
    "id":"kamlkmlkamskmalk",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"eso tilin",
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":{"etiqueta":"chamba", "color":"#ff0000"}, "prioridad":"alta" }
}
adios:agenda = {
    "id":"fwfwfsscd",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"noc",
    "start": { "date":(date.today()+timedelta(days=1)).__str__() },
    "end": { "date":(date.today()+timedelta(days=1)).__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":{"etiqueta":"estudio", "color":"#00ff00"}, "prioridad":"alta" }
}

njkadaskd:agenda = {
    "id":"jdsdnjas",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"sepa esto es d prueba",
    "start": { "date":(date.today()+timedelta(days=2)).__str__() },
    "end": { "date":(date.today()+timedelta(days=2)).__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":{"etiqueta":"personal", "color":"#0000ff"}, "prioridad":"alta" }
}

transparente:agenda = {
    "id":"soy transparente",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"jhdsdkfhddjjdjdjdjd",
    "start": { "dateTime":(datetime.today()+timedelta(days=3)).__str__(), "timeZone":"America/Mexico_City" },
    "end": { "dateTime":(datetime.today()+timedelta(days=3, hours=2)).__str__(), "timeZone":"America/Mexico_City" },
    "transparency":"transparent",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":{"etiqueta":"personal", "color":"#0000ff"}, "prioridad":"alta" }
}

todo:actividades_response = { "defaultReminders":[{ "method":"popup", "minutes":2 }], "items": [ hola, adios, njkadaskd, transparente ] }

print(todo)

sortCalendar(todo["items"], { "inicio":datetime.now(), "fin":datetime.now()+timedelta(hours=3) })