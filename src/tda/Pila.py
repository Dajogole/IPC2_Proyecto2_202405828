from .Nodo import Nodo

class Pila:
    __slots__ = ("tope", "_len")

    def __init__(self):
        self.tope = None
        self._len = 0

    def apilar(self, valor):
        nuevo = Nodo(valor)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self._len += 1

    def desapilar(self):
        if self.tope is None:
            return None
        valor = self.tope.valor
        self.tope = self.tope.siguiente
        self._len -= 1
        return valor

    def esta_vacia(self):
        return self.tope is None

    def __len__(self):
        return self._len
