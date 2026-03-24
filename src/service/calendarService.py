from copy import deepcopy
from datetime import date, datetime, time, timedelta
from typing import TypedDict
from src.model.calendarModel import Agenda, Candidato, RangoTiempo, RangoTiempoDt

# DICCIONARIOS DE APOYO

class RestriccionesEtiquetas(TypedDict): # no se usa por el momento
    tag:int
    horario:RangoTiempo

# FUNCIONES DE APOYO

def convertDate(fecha:str, tiempo:time) -> datetime:
    fecha_parsed: date = date.strptime( fecha, "%Y-%m-%d" )
    return datetime.combine( date=fecha_parsed, time=tiempo )

# -------------------------------------------------------------------------------

def convertStrToDt(fecha:str) -> datetime:
    return datetime.fromisoformat(fecha)

# -------------------------------------------------------------------------------

def getStartEnd(tarea:Agenda, inicioDia:time, finDia:time, inicio_descanso:time | None = None, fin_descanso:time | None = None, gap:int | None = None) -> tuple[datetime, datetime]:
    if tarea.start.dateTime:
        assert tarea.end.dateTime
        inicio: datetime = convertStrToDt( fecha=tarea.start.dateTime ).replace( tzinfo=None )
        fin: datetime = convertStrToDt( fecha=tarea.end.dateTime ).replace( tzinfo=None )
    else:
        assert tarea.start.date and tarea.end.date
        if inicio_descanso is not None:
            assert fin_descanso is not None and gap is not None
            inicio_descanso_nuevo: time = ( datetime.combine( date=date.today(), time=inicio_descanso ) + timedelta( minutes=gap ) ).time()
            fin_descanso_nuevo: time = ( datetime.combine( date=date.today(), time=fin_descanso ) ).time()
            inicio:datetime = convertDate( fecha=tarea.start.date, tiempo=inicio_descanso_nuevo )
            fin:datetime = convertDate( fecha=tarea.start.date, tiempo=fin_descanso_nuevo )
        else:
            inicio:datetime = convertDate( fecha=tarea.start.date, tiempo=inicioDia )
            fin:datetime = convertDate( fecha=tarea.start.date, tiempo=finDia )
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
) -> Candidato:

    # para actividades que tomen todo el dia
    inicioDia: time = time( hour=0, minute=0, second=0 )
    finDia: time = time( hour=23, minute=59, second=59)

    # para convertir la cadena de entrada del tiempo de descanso a un time
    formato_hora = "%H : %M : %S"
    hora_inicio_descanso: time = datetime.strptime(tiempo_descanso["inicio"], formato_hora).time()
    hora_fin_descanso: time = datetime.strptime(tiempo_descanso["fin"], formato_hora).time()
    
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
            inicio, fin = getStartEnd(tarea=e, inicioDia=inicioDia, finDia=finDia)
            puntaje_duracion = -(fin-inicio).total_seconds()
        
        return (puntaje_etiquetas, puntaje_prioridad, puntaje_duracion)



    actividades_estaticas: list[Agenda] = []
    actividades_libres: list[Agenda] = []

    tiempo_libre: list[RangoTiempoDt] = [] # no sé como manejarlo, entiendo que lo mejor seria tenerlo pero que tal si se acomodan las tareas alrededor del tiempo ocupado
    tiempo_ocupado: list[RangoTiempoDt] = []

    for actividad in actividades:
        if actividad.transparency == "opaque":
            inicio, fin = getStartEnd(tarea=actividad, inicioDia=inicioDia, finDia=finDia)
            tiempo_ocupado.append({ "inicio":inicio, "fin":fin })
            actividades_estaticas.append(actividad)
        else:
            actividades_libres.append(actividad)
        
    actividades_libres.sort(key=orderTasks) # este se deberia de acomodar dps siento yo

    madrugada: datetime = datetime.combine(date.today(), inicioDia)
    fin_madrugada: datetime = datetime.combine(date.today(), hora_inicio_descanso)
    tiempo_ocupado.append({ "inicio":madrugada, "fin":fin_madrugada })

    for i in range(dias_contemplados): # lo queria hacer funcion de apoyo pero ya era quemarme mucho el coco
        dia_actual: date = date.today() + timedelta(days=i)
        dia_siguiente: date = dia_actual + timedelta(days=1)

        inicio_descanso: datetime = datetime.combine(date=dia_actual, time=hora_fin_descanso)
        fin_descanso: datetime = datetime.combine(date=dia_siguiente, time=hora_inicio_descanso)

        tiempo_ocupado.append({"inicio":inicio_descanso, "fin":fin_descanso})
    
    tiempo_ocupado = mergeTimes(tiempos=tiempo_ocupado)

    dia_inicio: datetime = max(fin_madrugada+timedelta(minutes=gap), datetime.now()+timedelta(minutes=gap)) # se usa fin_madrugada por que es el mismo valor que se utilizaria
    dia_limite: datetime = datetime.combine(date=date.today() + timedelta(days=dias_contemplados), time=time(hour=23, minute=59, second=59))

    tiempo_libre = getFreeTime(tiempo_ocupado=tiempo_ocupado, inicio=dia_inicio, fin=dia_limite)



    def judgeCandidate(universo:Candidato) -> float:
        puntaje: float = 0.0

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
                inicio, fin = getStartEnd(tarea=tarea, inicioDia=inicioDia, finDia=finDia)
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
        universos_Candidato: list[Candidato] = []
        inicio, fin = getStartEnd(tarea=tarea, inicioDia=inicioDia, finDia=finDia, inicio_descanso=hora_inicio_descanso, fin_descanso=hora_fin_descanso, gap=gap)
        duracion_tarea: float = (fin-inicio).total_seconds()

        for universo in Candidatos:
            universo_malo: Candidato = deepcopy(universo)
            universo_malo.tareas_no_agendadas.append(tarea)
            universo_malo.puntaje = judgeCandidate(universo=universo_malo)
            universos_Candidato.append(universo_malo)
            
            for i, hueco in enumerate(universo.tiempo_libre_restante):
                duracion_hueco: float = (hueco["fin"]-hueco["inicio"]).total_seconds()
                if duracion_tarea <= duracion_hueco:
                    universo_nuevo: Candidato = deepcopy(universo)
                    tarea_clon: Agenda = deepcopy(tarea)

                    tarea_clon.start.dateTime = hueco["inicio"].isoformat()
                    tarea_clon.end.dateTime = (hueco["inicio"] + timedelta(seconds=duracion_tarea)).isoformat()

                    universo_nuevo.tareas_agendadas.append(tarea_clon)

                    universo_nuevo.tiempo_libre_restante = updateBusyTime(
                        hueco_libre=universo_nuevo.tiempo_libre_restante,
                        indice=i,
                        tiempo_restado=substractTime(hueco=hueco, duracion=duracion_tarea, gap=gap)
                    )
                    universo_nuevo.puntaje = judgeCandidate(universo=universo_nuevo)
                    universos_Candidato.append(universo_nuevo)
                    break
        Candidatos = sorted(universos_Candidato, key= lambda x:x.puntaje, reverse=True)[0:ancho_haz]

    ganador: Candidato = Candidatos[0]
    return ganador