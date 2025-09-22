import xml.etree.ElementTree as ET
from tda.Lista import ListaEnlazada
from domain.Invernadero import Invernadero
from domain.Planta import Planta
from domain.Dron import Dron
from domain.PlanRiego import PlanRiego

class ParserXML:
    def __init__(self, ruta:str):
        self._ruta = ruta
        self._invernaderos = ListaEnlazada()  
        self._drones_catalogo = ListaEnlazada()  

    def invernaderos(self): return self._invernaderos

    def parse(self):
        tree = ET.parse(self._ruta)
        root = tree.getroot()

     
        for n in root.iter():
            if n.tag == "listaDrones":
                for d in n:
                    if d.tag == "dron":
                        self._drones_catalogo.append( (int(d.attrib["id"]), d.attrib["nombre"]) )

      
        for n in root.iter():
            if n.tag == "invernadero":
                nombre = n.attrib["nombre"]
                numH = 0; pxh = 0
                for c in n:
                    if c.tag=="numeroHileras": numH = int(c.text.strip())
                    if c.tag=="plantasXhilera": pxh = int(c.text.strip())
                inv = Invernadero(nombre, numH, pxh)

               
                for c in n:
                    if c.tag=="listaPlantas":
                        for p in c:
                            if p.tag=="planta":
                                hil=int(p.attrib["hilera"]); pos=int(p.attrib["posicion"])
                                li=float(p.attrib["litrosAgua"]); gr=float(p.attrib["gramosFertilizante"])
                                nm=(p.text or "").strip()
                                inv.hilera(hil).agregar_planta(Planta(hil,pos,li,gr,nm))

         
                for c in n:
                    if c.tag=="asignacionDrones":
                        for d in c:
                            if d.tag=="dron":
                                did=int(d.attrib["id"]); hl=int(d.attrib["hilera"])
                                nombre_d = None
                                for par in self._drones_catalogo:
                                    if par[0]==did: nombre_d = par[1]
                                if nombre_d is None: nombre_d = f"DR{did:02d}"
                                inv.agregar_dron(Dron(did, nombre_d, hl))

                
                for c in n:
                    if c.tag=="planesRiego":
                        for p in c:
                            if p.tag=="plan":
                                plan = PlanRiego(p.attrib["nombre"])
                                plan.cargar_desde_cadena(p.text or "")
                                if not hasattr(inv, "_planes"):
                                    inv._planes = ListaEnlazada()
                                inv._planes.append(plan)

                self._invernaderos.append(inv)
        return self

