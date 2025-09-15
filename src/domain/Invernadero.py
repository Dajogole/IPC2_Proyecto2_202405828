from tda.Lista import ListaEnlazada
from domain.Hilera import Hilera

class Invernadero:
    def __init__(self, nombre:str, numero_hileras:int, plantas_x_hilera:int):
        self._nombre = nombre
        self._numH = numero_hileras
        self._pxh = plantas_x_hilera
        self._hileras = ListaEnlazada()  
        self._drones = ListaEnlazada()   
       
        k=1
        while k<=numero_hileras:
            self._hileras.append(Hilera(k))
            k+=1

    def nombre(self): return self._nombre
    def numero_hileras(self): return self._numH
    def plantas_x_hilera(self): return self._pxh
    def hileras(self): return self._hileras
    def drones(self): return self._drones

    def hilera(self, numero:int):
        for h in self._hileras:
            if h.numero()==numero: return h
        return None

    def agregar_dron(self, dron):
        self._drones.append(dron)
