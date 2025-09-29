from .Nodo import Nodo

class ListaSimple:
    __slots__ = ("cabeza", "cola", "_len")

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._len = 0

    def __len__(self):
        return self._len

    def esta_vacia(self):
        return self.cabeza is None

    def append(self, valor):
        nuevo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self._len += 1
        return nuevo

    def obtener(self, idx):
        # idx >= 0
        i = 0
        actual = self.cabeza
        while actual is not None:
            if i == idx:
                return actual.valor
            i += 1
            actual = actual.siguiente
        return None

    def primero(self):
        return self.cabeza.valor if self.cabeza is not None else None

    def ultimo(self):
        return self.cola.valor if self.cola is not None else None

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def clear(self):
        self.cabeza = None
        self.cola = None
        self._len = 0
