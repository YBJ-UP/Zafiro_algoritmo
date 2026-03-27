# Repositorio del algoritmo de organización del proyecto Zafiro
## Objetivo
Este algoritmo está desarrollado con el fin de otorgarle a los usuarios de [Zafiro](https://zafiro.digital) una mejor experiencia de organización, siendo esto a través de una herramienta configurable que ordene y organice sus actividades de manera rápida, eficiente y automática.
## Herramientas utilizadas
Algoritmo de Beam Search desarrollado en Python.  
Librerías de Python utilizadas:
- `fastapi`
- `uvicorn`
- `pydantic`
- `pyjwt`
- `python-dotenv`

Servicio desplegado en render.
## Endpoints
El servicio solamente cuenta con dos endpoints:  
```
/api/health # verifica que la API esté funcionando
/api/sort # función principal del servicio
```
[Documentación de endpoints](https://zafiro-algoritmo.onrender.com/docs) con Swagger.
## Datos
Este servicio solamente recibe datos cifrados con jwt, los cuales son los siguientes (estos no son los nombres reales):
```
config: # paramétros de configuración
	tiempo de descanso # cuando se va a dormir y cuando despierta el usuario
	dias contemplados # con cuantos dias va a atrabajar el servicio
	espacio # cuanto tiempo se deja entre actividad
	etiqueta # qué etiqueta se pondrá primero
	largas primero # si se pondrán primero las tareas largas

calendario:
	recordatorios predeterminados[]:
		metodo # si el recordatorio se envia por correo u otro método
		minutos # cuántos minutos antes de la fecha de la actividad
	items[]: # basado en los objetos de la API de Google Calendar
		id
		fecha_creacion
		fecha_actualizacion
		resumen
		inicio
		fin
		transparencia
		recordatorios
		extras:
			prioridad
			etiqueta
```
## Planes a futuro
- Se planea añadir el parámetro  `restricciones de etiqueta`, que definirá horarios específicos para ciertas etiquetas.
- Se planea que se puedan priorizar varias etiquetas a la vez en vez de solo una.
- Se planea poder dar un espacio adicional al comienzo del día.


