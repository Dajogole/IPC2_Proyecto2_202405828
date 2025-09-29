from __future__ import annotations
from typing import Optional

class PasoPlan:
    __slots__ = ("hilera", "posicion")
    def __init__(self, hilera: int, posicion: int):
        self.hilera = int(hilera)
        self.posicion = int(posicion)

class Planta:
    __slots__ = ("hilera", "posicion", "litros", "gramos", "nombre")
    def __init__(self, hilera: int, posicion: int, litros: float, gramos: float, nombre: str):
        self.hilera = int(hilera)
        self.posicion = int(posicion)
        self.litros = float(litros)
        self.gramos = float(gramos)
        self.nombre = nombre

class Dron:
    __slots__ = ("id", "nombre", "hilera", "posicion", "terminado", "agua_acum", "fert_acum")
    def __init__(self, id: int, nombre: str):
        self.id = int(id)
        self.nombre = nombre
        self.hilera: Optional[int] = None
        self.posicion: int = 0  
        self.terminado: bool = False
        self.agua_acum: float = 0.0
        self.fert_acum: float = 0.0

class Hilera:
    __slots__ = ("numero", "plantas") 
    def __init__(self, numero: int, plantas_mapa):
        self.numero = int(numero)
        self.plantas = plantas_mapa

class PlanRiego:
    __slots__ = ("nombre", "pasos")  
    def __init__(self, nombre: str, pasos_lista):
        self.nombre = nombre
        self.pasos = pasos_lista

class Invernadero:
    __slots__ = ("nombre", "numero_hileras", "plantas_x_hilera", "hileras", "asignaciones", "planes")
    def __init__(self, nombre: str, numero_hileras: int, plantas_x_hilera: int, hileras_mapa, asignaciones_mapa, planes_lista):
        self.nombre = nombre
        self.numero_hileras = int(numero_hileras)
        self.plantas_x_hilera = int(plantas_x_hilera)
        self.hileras = hileras_mapa    
        self.asignaciones = asignaciones_mapa  
        self.planes = planes_lista     

class InstruccionDron:
    __slots__ = ("dron_nombre", "accion")
    def __init__(self, dron_nombre: str, accion: str):
        self.dron_nombre = dron_nombre
        self.accion = accion

class InstruccionesTiempo:
    __slots__ = ("segundos", "acciones")  
    def __init__(self, segundos: int, acciones_lista):
        self.segundos = int(segundos)
        self.acciones = acciones_lista

class ResultadoPlan:
    __slots__ = ("tiempo_optimo", "agua_total", "fert_total", "por_dron", "timeline")
    def __init__(self, tiempo_optimo: int, agua_total: float, fert_total: float, por_dron_mapa, timeline_lista):
        self.tiempo_optimo = int(tiempo_optimo)
        self.agua_total = float(agua_total)
        self.fert_total = float(fert_total)
        self.por_dron = por_dron_mapa 
        self.timeline = timeline_lista 

class ParNumeros:
    __slots__ = ("a", "b")
    def __init__(self, a: float, b: float):
        self.a = float(a)
        self.b = float(b)
