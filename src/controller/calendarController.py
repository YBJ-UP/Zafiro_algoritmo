from fastapi import HTTPException
from pydantic import BaseModel
from src.model.calendarModel import ActividadesResponse, Agenda, Candidato, RangoTiempo
from src.service.calendarService import sortCalendar

class Config(BaseModel):
    tiempo_descanso: RangoTiempo
    dias_contemplados:int = 7
    gap:int = 15
    tag:int | None = None
    long_first:bool = False

class CalendarResponse(BaseModel):
    config:Config
    calendar:ActividadesResponse

def sortCalendarController(data:CalendarResponse):
    try:
        actividades: list[Agenda] = data.calendar.items # Intenta extraer los datos de agenda y configuracion de los datos recibidos
        config: Config = data.config

        if not actividades or not config: # Da un error en caso de que no vengan los datos completos
            raise HTTPException(status_code=400, detail="Datos erróneos o incompletos")

        ganador: Candidato = sortCalendar( # Si vienen los datos completos, llama a la función principal
            actividades= actividades,
            tiempo_descanso= config.tiempo_descanso,
            dias_contemplados= config.dias_contemplados,
            gap= config.gap,
            tag= config.tag,
            long_first= config.long_first
        )

        tareas_agendadas_json: list[Agenda] = [Agenda.model_dump(self=tarea, exclude_none=True) for tarea in ganador.tareas_agendadas] # Convierte las listas de tareas en diccionarios
        tareas_no_agendadas_json: list[Agenda] = [Agenda.model_dump(self=tarea, exclude_none=True) for tarea in ganador.tareas_no_agendadas]

        return {
            "status":"succes",
            "code":200,
            "tareas_agendadas": tareas_agendadas_json,
            "tareas_no_agendadas": tareas_no_agendadas_json
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)