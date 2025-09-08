from tda.Lista import ListaEnlazada

class Cola:
    def __init__(self):
        self._datos = ListaEnlazada()

    def __len__(self): return len(self._datos)
    def esta_vacia(self): return len(self)==0

    def encolar(self, x): self._datos.append(x)

    def desencolar(self):
        if self.esta_vacia(): return None
        return self._datos.remove_at(0)

    def frente(self):
        if self.esta_vacia(): return None
        return self._datos.get(0)
