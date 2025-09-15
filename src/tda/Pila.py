from tda.Lista import ListaEnlazada

class Pila:
    def __init__(self):
        self._datos = ListaEnlazada()
    def __len__(self): return len(self._datos)
    def esta_vacia(self): return len(self)==0
    def apilar(self, x): self._datos.append(x)
    def desapilar(self): 
        if self.esta_vacia(): return None
        return self._datos.remove_at(len(self._datos)-1)
    def cima(self):
        if self.esta_vacia(): return None
        return self._datos.get(len(self._datos)-1)
