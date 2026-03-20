from copy import deepcopy
from datetime import date, datetime, time, timedelta
from typing import TypedDict
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.calendarModel import Agenda, ActividadesResponse, Candidato, DateDict, EtiquetasDict, ExtrasDict, RangoTiempo, RangoTiempoDt, ReminderDict

# DICCIONARIOS DE APOYO

class RestriccionesEtiquetas(TypedDict): # no se usa por el momento
    tag:int
    horario:RangoTiempo

# FUNCIONES DE APOYO

def convertDate(fecha:str, tiempo:time) -> datetime:
    fecha_parsed: date = date.strptime( fecha, "%Y-%m-%d" )
    return datetime.combine(fecha_parsed, tiempo)

# -------------------------------------------------------------------------------

def convertStrToDt(fecha:str) -> datetime:
    return datetime.fromisoformat(fecha)

# -------------------------------------------------------------------------------

def getStartEnd(tarea:Agenda, inicioDia:time, finDia:time) -> tuple[datetime, datetime]:
    if tarea.start.dateTime:
        assert tarea.end.dateTime
        inicio: datetime = convertStrToDt(tarea.start.dateTime)
        fin: datetime = convertStrToDt(tarea.end.dateTime)
    else:
        assert tarea.start.date and tarea.end.date
        inicio = convertDate(tarea.start.date, inicioDia)
        fin = convertDate(tarea.end.date, finDia)
    return (inicio, fin)

# -------------------------------------------------------------------------------

def mergeTimes(tiempos:list[RangoTiempoDt]) -> list[RangoTiempoDt]:
    if not tiempos:
        return []
    tiempo_reordenado:list[RangoTiempoDt] = sorted(tiempos, key=lambda e:e["inicio"])

    fusionados:list[RangoTiempoDt] = [tiempo_reordenado[0]]

    for tarea in tiempo_reordenado[1:]:
        tarea_previa: RangoTiempoDt = fusionados[-1]
        if tarea["inicio"] <= tarea_previa["fin"]:
            tarea_previa["fin"] = max(tarea["fin"], tarea_previa["fin"])
        else:
            fusionados.append(tarea)
    return fusionados

# -------------------------------------------------------------------------------

def getFreeTime(tiempo_ocupado:list[RangoTiempoDt], inicio:datetime, fin:datetime) -> list[RangoTiempoDt]:
    indice: datetime = inicio

    tiempo_reordenado:list[RangoTiempoDt] = []

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

def substractTime(hueco:RangoTiempoDt, duracion:float, gap:int) -> RangoTiempoDt | None:
    fin_tarea: datetime = hueco["inicio"] + timedelta(seconds=duracion)
    inicio_hueco_nuevo: datetime = fin_tarea + timedelta(minutes=gap)

    if inicio_hueco_nuevo < hueco["fin"]:
        return { "inicio":inicio_hueco_nuevo, "fin":hueco["fin"] }
    return None

# -------------------------------------------------------------------------------

def updateBusyTime(hueco_libre:list[RangoTiempoDt], indice:int, tiempo_restado: RangoTiempoDt | None) -> list[RangoTiempoDt]:
    hueco_libre_copia: list[RangoTiempoDt] = hueco_libre[:]
    if tiempo_restado is not None:
        hueco_libre_copia[indice] = tiempo_restado
    else:
        hueco_libre_copia.pop(indice)
    return hueco_libre_copia

# -------------------------------------------------------------------------------


# FUNCIÓN PRINCIPAL

def sortCalendar(
        actividades:list[Agenda],
        tiempo_descanso:RangoTiempo, # este se convertirá en un arreglo de dateTime
        dias_contemplados:int = 7, # hasta cuantos dias se puede recorrer una tarea supongo
        gap:int = 15,
        tag:int | None = None, # de acuerdo a qué etiqueta se va a ordenar
        long_first:bool = False,
        tag_restriction:RestriccionesEtiquetas | None = None #podria venir como un arreglo de restricciones pero por los tiempos capaz y ni siquiera se implemente
) -> Candidato: #none por ahora

    # para actividades que tomen todo el dia
    inicioDia:time = time(0,0,0)
    finDia:time = time(23,59,59)
    
    def orderTasks(e:Agenda):
        puntaje_prioridad:int = 0
        puntaje_etiquetas:int = 0
        puntaje_duracion:float = 0

        match e.extras.prioridad:
            case "alta":
                puntaje_prioridad+=1
            case "media":
                puntaje_prioridad+=2
            case "baja":
                puntaje_prioridad+=3

        if tag is not None:
            if e.extras.etiquetas.etiqueta != tag:
                puntaje_etiquetas+=1

        if long_first:
            inicio, fin = getStartEnd(e, inicioDia, finDia)
            puntaje_duracion = -(fin-inicio).total_seconds()
        
        return (puntaje_etiquetas, puntaje_prioridad, puntaje_duracion)



    actividades_estaticas:list[Agenda] = []
    actividades_libres:list[Agenda] = []

    tiempo_libre:list[RangoTiempoDt] = [] # no sé como manejarlo, entiendo que lo mejor seria tenerlo pero que tal si se acomodan las tareas alrededor del tiempo ocupado
    tiempo_ocupado:list[RangoTiempoDt] = []

    for actividad in actividades:
        if actividad.transparency == "opaque":
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



    def judgeCandidate(universo:Candidato) -> float:
        puntaje:float = 0.0

        for tarea in universo.tareas_agendadas:
            match tarea.extras.prioridad:
                case "alta":
                    puntaje += 3
                case "media":
                    puntaje += 2
                case "baja":
                    puntaje += 1

            if tag is not None:
                if tarea.extras.etiquetas.etiqueta == tag:
                    puntaje +=5

            if long_first:
                inicio, fin = getStartEnd(tarea, inicioDia, finDia)
                puntaje += (fin-inicio).total_seconds()/3600
        
        for tarea in universo.tareas_no_agendadas:
            match tarea.extras.prioridad:
                case "alta":
                    puntaje -= 6
                case "media":
                    puntaje -= 4
                case "baja":
                    puntaje -= 2

            if tag is not None:
                if tarea.extras.etiquetas.etiqueta == tag:
                    puntaje -= 10

        return puntaje
    
    ancho_haz = 5

    Candidato_inicial = Candidato()
    Candidato_inicial.tiempo_libre_restante = tiempo_libre
    Candidatos: list[Candidato] = [ Candidato_inicial ]

    for tarea in actividades_libres:
        universos_Candidato:list[Candidato] = []
        inicio, fin = getStartEnd(tarea, inicioDia, finDia)
        duracion_tarea: float = (fin-inicio).total_seconds()

        for universo in Candidatos:
            universo_malo: Candidato = deepcopy(universo)
            universo_malo.tareas_no_agendadas.append(tarea)
            universo_malo.puntaje = judgeCandidate(universo_malo)
            universos_Candidato.append(universo_malo)
            
            for i, hueco in enumerate(universo.tiempo_libre_restante):
                duracion_hueco: float = (hueco["fin"]-hueco["inicio"]).total_seconds()
                if duracion_tarea <= duracion_hueco:
                    universo_nuevo: Candidato = deepcopy(universo)
                    tarea_clon: Agenda = deepcopy(tarea)

                    tarea_clon.start.dateTime = hueco["inicio"].__str__()
                    tarea_clon.end.dateTime = (hueco["inicio"] + timedelta(seconds=duracion_tarea)).__str__()

                    universo_nuevo.tareas_agendadas.append(tarea_clon)

                    universo_nuevo.tiempo_libre_restante = updateBusyTime(
                        universo_nuevo.tiempo_libre_restante,
                        i,
                        substractTime(hueco, duracion_tarea, gap)
                    )
                    universo_nuevo.puntaje = judgeCandidate(universo_nuevo)
                    universos_Candidato.append(universo_nuevo)
                    break
        Candidatos = sorted(universos_Candidato, key= lambda x:x.puntaje, reverse=True)[0:ancho_haz]


    ganador: Candidato = Candidatos[0]
    print(f"Puntaje del ganador: {ganador.puntaje}")
    print(f"Actividades seleccionadas:\n{ganador.tareas_agendadas}")
    print(f"Actividades no seleccionadas:\n{ganador.tareas_no_agendadas}")
    print(f"Tiempo libre restante:\n{ganador.tiempo_libre_restante}")
    return ganador



hola_raw = {
    "id":"kamlkmlkamskmalk",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"eso tilin",
    "start": { "date":date.today().__str__() },
    "end": { "date":date.today().__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":{"etiqueta":3, "color":"#ff0000"}, "prioridad":"alta" }
}
hola = Agenda(**hola_raw)

adios:Agenda = Agenda(
    id="fwfwfsscd",
    created=datetime.now().__str__(),
    updated=datetime.now().__str__(),
    summary="noc",
    start= DateDict( dateTime=(datetime.today()+timedelta(days=1, hours=9)).__str__() ),
    end= DateDict( dateTime=(datetime.today()+timedelta(days=1, hours=12)).__str__() ),
    transparency="transparent",
    reminders= ReminderDict(useDefault=True),
    extras= ExtrasDict( etiquetas=EtiquetasDict(etiqueta=1, color="#00ff00"), prioridad="media" )
)

njkadaskd:Agenda = Agenda(**{
    "id":"jdsdnjas",
    "created":datetime.now().__str__(),
    "updated":datetime.now().__str__(),
    "summary":"sepa esto es d prueba",
    "start": { "date":(date.today()+timedelta(days=2)).__str__() },
    "end": { "date":(date.today()+timedelta(days=2)).__str__() },
    "transparency":"opaque",
    "reminders": { "useDefault":True },
    "extras": { "etiquetas":{"etiqueta":2, "color":"#0000ff"}, "prioridad":"alta" }
})

transparente:Agenda = Agenda(
    id="soy transparente",
    created=datetime.now().__str__(),
    updated=datetime.now().__str__(),
    summary="jhdsdkfhddjjdjdjdjd",
    start= DateDict( dateTime=(datetime.today()+timedelta(days=3)).__str__(), timeZone="America/Mexico_City" ),
    end= DateDict( dateTime=(datetime.today()+timedelta(days=3, hours=2)).__str__(), timeZone="America/Mexico_City" ),
    transparency="transparent",
    reminders= ReminderDict(useDefault=True),
    extras= ExtrasDict( etiquetas=EtiquetasDict(**{"etiqueta":2, "color":"#0000ff"}), prioridad="alta" )
)

todo:ActividadesResponse = ActividadesResponse( defaultReminders = [{ "method":"popup", "minutes":1 }], items = [ hola, adios, njkadaskd, transparente ] )

sortCalendar(todo.items, { "inicio":time(hour=8), "fin":time(hour=22) }, tag=1, long_first=True)