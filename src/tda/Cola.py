from .Nodo import Nodo

class Cola:
    __slots__ = ("frente", "final", "_len")

    def __init__(self):
        self.frente = None
        self.final = None
        self._len = 0

    def encolar(self, valor):
        nuevo = Nodo(valor)
        if self.final is None:
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self._len += 1

    def desencolar(self):
        if self.frente is None:
            return None
        valor = self.frente.valor
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self._len -= 1
        return valor

    def esta_vacia(self):
        return self.frente is None

    def __len__(self):
        return self._len
