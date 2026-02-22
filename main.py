from dataclasses import dataclass
from typing import Optional,TypedDict, Literal
# peleandome por ponerle tipado a la cosa esta

class persona(TypedDict): #basicamente un tipo (o es una interfaz? ni se q tienen d diferente)
    nombre:str
    apellidos:str
    fecha_nacimiento:None #noc como poner fechas aca pero bueno
    literal:Literal[1, 2, 3, 4]
    opcional:Optional[int]
    arreglo:list[bool]

yo:persona = {
    "nombre":"yael",
    "apellidos":"betanzos jimenez",
    "fecha_nacimiento":None,
    "arreglo":[],
    "literal":3,
    "opcional":None
}

@dataclass
class persona_dataclass:
    nombre:str
    apellidos:str
    literal:Literal[1,2,3,4]
    arreglo:list[bool]
    fecha_nacimiento:None = None
    opcional:Optional[int] = None #a estos se les puede poner valores predeterminados para q no de lata al no ponerlos al construirlos, a diferencia de los typeddict que no dejan hacer eso

yo2 = persona_dataclass("yo", "yppp", 3, [], opcional=2783)

def saludar(nombre:Optional[str] = None): #me hace ruido que no sea como en ts pero bueno
    return f"hola ${nombre}" if nombre else "dime tu nombre" #analogo al a? b : c de ts


print(saludar())
print(yo["nombre"])
print(yo2.nombre)