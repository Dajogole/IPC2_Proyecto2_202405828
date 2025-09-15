from tda.Lista import ListaEnlazada

class Hilera:
    def __init__(self, numero:int):
        self._numero = numero
        self._plantas = ListaEnlazada()  

    def numero(self): return self._numero
    def plantas(self): return self._plantas

    def agregar_planta(self, planta):
        self._plantas.append(planta)

    def planta_en(self, posicion:int):
     
        for p in self._plantas:
            if p.posicion() == posicion:
                return p
        return None
