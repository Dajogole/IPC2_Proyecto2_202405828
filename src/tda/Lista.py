from tda.Nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._n = 0

    def __len__(self): return self._n
    def esta_vacia(self): return self._n == 0

    def append(self, valor):
        nodo = Nodo(valor)
        if self._cabeza is None:
            self._cabeza = self._cola = nodo
        else:
            self._cola.siguiente = nodo
            nodo.anterior = self._cola
            self._cola = nodo
        self._n += 1

    def prepend(self, valor):
        nodo = Nodo(valor)
        if self._cabeza is None:
            self._cabeza = self._cola = nodo
        else:
            nodo.siguiente = self._cabeza
            self._cabeza.anterior = nodo
            self._cabeza = nodo
        self._n += 1

    def get(self, i:int):
        if i < 0 or i >= self._n: raise IndexError("índice fuera de rango")
        cur = self._cabeza
        k = 0
        while k < i:
            cur = cur.siguiente
            k += 1
        return cur.valor

    def remove_at(self, i:int):
        if i < 0 or i >= self._n: raise IndexError("índice fuera de rango")
        cur = self._cabeza
        k = 0
        while k < i:
            cur = cur.siguiente
            k += 1
        ant, sig = cur.anterior, cur.siguiente
        if ant: ant.siguiente = sig
        else: self._cabeza = sig
        if sig: sig.anterior = ant
        else: self._cola = ant
        self._n -= 1
        return cur.valor

    def find(self, pred):  
        cur = self._cabeza
        while cur:
            if pred(cur.valor): return cur.valor
            cur = cur.siguiente
        return None

    def __iter__(self):
        cur = self._cabeza
        while cur:
            yield cur.valor
            cur = cur.siguiente
