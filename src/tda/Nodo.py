class Nodo:
    __slots__ = ("valor", "siguiente")
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class NodoKV:
    __slots__ = ("k", "v", "siguiente")
    def __init__(self, k, v):
        self.k = k
        self.v = v
        self.siguiente = None
