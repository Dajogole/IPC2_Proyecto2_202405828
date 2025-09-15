from tda.Lista import ListaEnlazada

class PlanPaso:
    def __init__(self, hilera:int, posicion:int):
        self.hilera = hilera
        self.posicion = posicion

class PlanRiego:
    def __init__(self, nombre:str):
        self._nombre = nombre
        self._pasos = ListaEnlazada()

    def nombre(self): return self._nombre
    def pasos(self): return self._pasos

    
    def cargar_desde_cadena(self, cadena:str):
        i, n = 0, len(cadena)
        while i < n:
        
            while i < n and cadena[i] not in ('H','h'): i += 1
            if i>=n: break
            i+=1
            h=0
            while i<n and cadena[i].isdigit():
                h = h*10 + (ord(cadena[i])-48); i+=1
           
            while i<n and cadena[i] not in ('P','p'): i+=1
            if i<n and (cadena[i] in ('P','p')):
                i+=1
                p=0
                while i<n and cadena[i].isdigit():
                    p = p*10 + (ord(cadena[i])-48); i+=1
                if h>0 and p>0:
                    self._pasos.append(PlanPaso(h,p))
          
            while i<n and cadena[i] not in (','): i+=1
            if i<n and cadena[i]==',': i+=1
