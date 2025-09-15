class Planta:
    def __init__(self, hilera:int, posicion:int, litros:float, gramos:float, nombre:str):
        self._hilera = hilera
        self._pos = posicion
        self._litros = litros
        self._gramos = gramos
        self._nombre = nombre.strip()

    def hilera(self): return self._hilera
    def posicion(self): return self._pos
    def litros(self): return self._litros
    def gramos(self): return self._gramos
    def nombre(self): return self._nombre
