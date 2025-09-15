from tda.Cola import Cola

class Dron:
    def __init__(self, id:int, nombre:str, hilera:int):
        self._id = id
        self._nombre = nombre
        self._hilera = hilera
        self._pos = 0  
        self._litros = 0.0
        self._gramos = 0.0
        self._objetivos = Cola()  
        self._fin_empleado = False

    def id(self): return self._id
    def nombre(self): return self._nombre
    def hilera(self): return self._hilera
    def pos(self): return self._pos
    def set_pos(self, p): self._pos = p
    def litros(self): return self._litros
    def gramos(self): return self._gramos
    def sumar(self, l, g): self._litros += l; self._gramos += g
    def objetivos(self): return self._objetivos
    def marcar_fin(self): self._fin_empleado = True
    def fin_empleado(self): return self._fin_empleado
