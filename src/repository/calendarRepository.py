from copy import deepcopy
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
    inicio:time
    fin:time

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
    puntaje:float = 0.0

# FUNCIONES DE APOYO

def convertDate(fecha:str, tiempo:time) -> datetime:
    fecha_parsed: date = date.strptime( fecha, "%Y-%m-%d" )
    return datetime.combine(fecha_parsed, tiempo)

# -------------------------------------------------------------------------------

def convertStrToDt(fecha:str) -> datetime:
    return datetime.fromisoformat(fecha)

# -------------------------------------------------------------------------------

def getStartEnd(tarea:agenda, inicioDia:time, finDia:time) -> tuple[datetime, datetime]:
    if "dateTime" in tarea["start"]:
        assert "dateTime" in tarea["end"]
        inicio: datetime = convertStrToDt(tarea["start"]["dateTime"])
        fin: datetime = convertStrToDt(tarea["end"]["dateTime"])
    else:
        assert "date" in tarea["start"] and "date" in tarea["end"]
        inicio = convertDate(tarea["start"]["date"], inicioDia)
        fin = convertDate(tarea["end"]["date"], finDia)
    return (inicio, fin)

# -------------------------------------------------------------------------------

def mergeTimes(tiempos:list[rango_tiempo_dt]) -> list[rango_tiempo_dt]:
    if not tiempos:
        return []
    tiempo_reordenado:list[rango_tiempo_dt] = sorted(tiempos, key=lambda e:e["inicio"])

    fusionados:list[rango_tiempo_dt] = [tiempo_reordenado[0]]

    for tarea in tiempo_reordenado[1:]:
        tarea_previa: rango_tiempo_dt = fusionados[-1]
        if tarea["inicio"] <= tarea_previa["fin"]:
            tarea_previa["fin"] = max(tarea["fin"], tarea_previa["fin"])
        else:
            fusionados.append(tarea)
    return fusionados

# -------------------------------------------------------------------------------

def getFreeTime(tiempo_ocupado:list[rango_tiempo_dt], inicio:datetime, fin:datetime) -> list[rango_tiempo_dt]:
    indice: datetime = inicio

    tiempo_reordenado:list[rango_tiempo_dt] = []

    for rango in tiempo_ocupado:
        if rango["fin"] <= indice:
            continue
        if indice < rango["inicio"]:
            tiempo_reordenado.append({"inicio":indice, "fin":rango["inicio"]})
        indice = max(indice, rango["fin"])
    
    if indice < fin:
        tiempo_reordenado.append({"inicio":indice, "fin":fin})
    
    return tiempo_reordenado

# -------------------------------------------------------------------------------

def substractTime(hueco:rango_tiempo_dt, duracion:float, gap:int) -> rango_tiempo_dt | None:
    fin_tarea: datetime = hueco["inicio"] + timedelta(seconds=duracion)
    inicio_hueco_nuevo: datetime = fin_tarea + timedelta(minutes=gap)

    if inicio_hueco_nuevo < hueco["fin"]:
        return { "inicio":inicio_hueco_nuevo, "fin":hueco["fin"] }
    return None

# -------------------------------------------------------------------------------

def updateBusyTime(tiempo_ocupado:list[rango_tiempo_dt], indice:int, tiempo_restado: rango_tiempo_dt | None) -> list[rango_tiempo_dt]:
    tiempo_ocupado_copia: list[rango_tiempo_dt] = tiempo_ocupado[:]
    if tiempo_restado is not None:
        tiempo_ocupado_copia[indice] = tiempo_restado
    else:
        tiempo_ocupado_copia.pop(indice)
    return tiempo_ocupado_copia

# -------------------------------------------------------------------------------


# FUNCIÓN PRINCIPAL

def sortCalendar(
        actividades:list[agenda],
        tiempo_descanso:rango_tiempo, # este se convertirá en un arreglo de dateTime
        dias_contemplados:int = 7, # hasta cuantos dias se puede recorrer una tarea supongo
        gap:int = 15,
        tag:str | None = None, # de acuerdo a qué etiqueta se va a ordenar
        long_first:bool = False,
        tag_restriction:restricciones_etiquetas | None = None #podria venir como un arreglo de restricciones pero por los tiempos capaz y ni siquiera se implemente
) -> None: #none por ahora

    # para actividades que tomen todo el dia
    inicioDia:time = time(0,0,0)
    finDia:time = time(23,59,59)
    
    def orderTasks(e:agenda):
        puntaje_prioridad:int = 0
        puntaje_etiquetas:int = 0
        puntaje_duracion:float = 0

        match e["extras"]["prioridad"]:
            case "alta":
                puntaje_prioridad+=1
            case "media":
                puntaje_prioridad+=2
            case "baja":
                puntaje_prioridad+=3

        if tag is not None:
            if e["extras"]["etiquetas"]["etiqueta"] != tag:
                puntaje_etiquetas+=1

        if long_first:
            inicio, fin = getStartEnd(e, inicioDia, finDia)
            puntaje_duracion = -(fin-inicio).total_seconds()
        
        return (puntaje_etiquetas, puntaje_prioridad, puntaje_duracion)



    actividades_estaticas:list[agenda] = []
    actividades_libres:list[agenda] = []

    tiempo_libre:list[rango_tiempo_dt] = [] # no sé como manejarlo, entiendo que lo mejor seria tenerlo pero que tal si se acomodan las tareas alrededor del tiempo ocupado
    tiempo_ocupado:list[rango_tiempo_dt] = []

    for actividad in actividades:
        if actividad["transparency"] == "opaque":
            inicio, fin = getStartEnd(actividad, inicioDia, finDia)
            tiempo_ocupado.append({ "inicio":inicio, "fin":fin })
            actividades_estaticas.append(actividad)
        else:
            actividades_libres.append(actividad)
        
    actividades_libres.sort(key=orderTasks) # este se deberia de acomodar dps siento yo

    for i in range(dias_contemplados): # lo queria hacer funcion de apoyo pero ya era quemarme mucho el coco
        dia_actual: date = date.today() + timedelta(days=i)
        dia_siguiente: date = dia_actual + timedelta(days=1)

        inicio_descanso: datetime = datetime.combine(dia_actual, tiempo_descanso["fin"])
        fin_descanso: datetime = datetime.combine(dia_siguiente, tiempo_descanso["inicio"])

        tiempo_ocupado.append({"inicio":inicio_descanso, "fin":fin_descanso})
    
    tiempo_ocupado = mergeTimes(tiempo_ocupado)

    dia_inicio: datetime = datetime.now() + timedelta(minutes=gap)
    dia_limite: datetime = datetime.combine(date.today() + timedelta(days=dias_contemplados), time(hour=23, minute=59, second=59))

    tiempo_libre = getFreeTime(tiempo_ocupado, dia_inicio, dia_limite)



    def judgeCandidate(candidatos:candidato) -> float:
        puntaje:float = 0.0

        for tarea in candidatos.tareas_agendadas:
            match tarea["extras"]["prioridad"]:
                case "alta":
                    puntaje += 3
                case "media":
                    puntaje += 2
                case "baja":
                    puntaje += 1

            if tag is not None:
                if tarea["extras"]["etiquetas"]["etiqueta"] == tag:
                    puntaje +=5

            if long_first:
                inicio, fin = getStartEnd(tarea, inicioDia, finDia)
                puntaje += (fin-inicio).total_seconds()/3600
        
        for tarea in candidatos.tareas_no_agendadas:
            match tarea["extras"]["prioridad"]:
                case "alta":
                    puntaje -= 6
                case "media":
                    puntaje -= 4
                case "baja":
                    puntaje -= 2

            if tag is not None:
                if tarea["extras"]["etiquetas"]["etiqueta"] == tag:
                    puntaje -= 10

        return puntaje
    
    ancho_haz = 5

    candidato_inicial = candidato()
    candidato_inicial.tiempo_libre_restante = tiempo_libre
    candidatos: list[candidato] = [ candidato_inicial ]

    for tarea in actividades_libres:
        universos_candidato:list[candidato] = []
        inicio, fin = getStartEnd(tarea, inicioDia, finDia)
        duracion_tarea: float = (fin-inicio).total_seconds()

        for universo in candidatos:
            universo_malo = deepcopy(universo)
            universo_malo.tareas_no_agendadas.append(tarea)
            universo_malo.puntaje = judgeCandidate(universo)
            universos_candidato.append(universo_malo)
            
            for i, hueco in enumerate(universo.tiempo_libre_restante):
                duracion_hueco: float = (hueco["fin"]-hueco["inicio"]).total_seconds()
                if duracion_tarea <= duracion_hueco:
                    universo_nuevo: candidato = deepcopy(universo)
                    tarea_clon: agenda = deepcopy(tarea)

                    tarea_clon["start"]["dateTime"] = hueco["inicio"].__str__()
                    tarea_clon["end"]["dateTime"] = hueco["fin"].__str__()

                    universo_nuevo.tareas_agendadas.append(tarea_clon)

                    universo_nuevo.tiempo_libre_restante = updateBusyTime(
                        universo_nuevo.tiempo_libre_restante,
                        i,
                        substractTime(hueco, duracion_tarea, gap)
                    )
                    universo_nuevo.puntaje = judgeCandidate(universo_nuevo)
                    universos_candidato.append(universo_nuevo)
                    break
        


    print(ancho_haz)
    print(tiempo_ocupado, "\n")
    print(actividades_libres, "\n")
    print(tiempo_libre)



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
    "start": { "dateTime":(datetime.today()+timedelta(days=1, hours=9)).__str__() },
    "end": { "dateTime":(datetime.today()+timedelta(days=1, hours=12)).__str__() },
    "transparency":"transparent",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":{"etiqueta":"estudio", "color":"#00ff00"}, "prioridad":"media" }
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

sortCalendar(todo["items"], { "inicio":time(hour=8), "fin":time(hour=22) }, tag="estudio", long_first=True)