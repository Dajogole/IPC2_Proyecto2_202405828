from .Nodo import NodoKV

class Par:
    __slots__ = ("k", "v")
    def __init__(self, k, v):
        self.k = k
        self.v = v

class Mapa:
   
    __slots__ = ("cabeza", "cola", "_len")

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._len = 0

    def set(self, k, v):
        actual = self.cabeza
        while actual is not None:
            if actual.k == k:
                actual.v = v
                return
            actual = actual.siguiente
        nodo = NodoKV(k, v)
        if self.cabeza is None:
            self.cabeza = nodo
            self.cola = nodo
        else:
            self.cola.siguiente = nodo
            self.cola = nodo
        self._len += 1

    def get(self, k):
        actual = self.cabeza
        while actual is not None:
            if actual.k == k:
                return actual.v
            actual = actual.siguiente
        return None

    def contains(self, k):
        return self.get(k) is not None

    def __len__(self):
        return self._len

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield Par(actual.k, actual.v)
            actual = actual.siguiente

    def keys(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.k
            actual = actual.siguiente

    def values(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.v
            actual = actual.siguiente
