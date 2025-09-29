
import xml.etree.ElementTree as ET
from ..tda.Mapa import Mapa
from ..tda.ListaSimple import ListaSimple
from ..domain import Planta, Dron, Hilera, Invernadero, PlanRiego, PasoPlan
from ..core.Sistema import Sistema

class ParserXML:
    def __init__(self, sistema: Sistema):
        self.sistema = sistema

    def cargar_desde_archivo(self, ruta_xml: str):

        self.sistema.reset()

    
        drones_global = Mapa()

        invernaderos_lista = ListaSimple()


        inv_nombre = None
        inv_num_h = None
        inv_px_h = None
        inv_hileras = None
        inv_asignaciones = None
        inv_planes = None
        inv_plants_mapa = None  

        current_invernadero = None

        for event, elem in ET.iterparse(ruta_xml, events=("start", "end")):
            tag = elem.tag.strip()

            if event == "start":
                if tag == "invernadero":
                    inv_nombre = elem.attrib.get("nombre")
                    inv_hileras = Mapa()
                    inv_asignaciones = Mapa()
                    inv_planes = ListaSimple()
                    inv_plants_mapa = Mapa()

            else:

                if tag == "dron" and elem.attrib.get("nombre") is not None:

                    id_str = elem.attrib.get("id")
                    nombre = elem.attrib.get("nombre")
                    try:
                        idnum = int(id_str)
                    except:
                        idnum = id_str
                    drones_global.set(idnum, Dron(idnum, nombre))

                elif tag == "numeroHileras":
                    inv_num_h = int(elem.text.strip()) if elem.text else 0

                elif tag == "plantasXhilera":
                    inv_px_h = int(elem.text.strip()) if elem.text else 0

                elif tag == "planta":

                    hilera = int(elem.attrib.get("hilera"))
                    posicion = int(elem.attrib.get("posicion"))
                    litros = float(elem.attrib.get("litrosAgua"))
                    gramos = float(elem.attrib.get("gramosFertilizante"))
                    nombre_planta = (elem.text or "").strip()

                    planta = Planta(hilera, posicion, litros, gramos, nombre_planta)

                    mapa_pl_hilera = inv_plants_mapa.get(hilera)
                    if mapa_pl_hilera is None:
                        from ..tda.Mapa import Mapa as _Mapa
                        mapa_pl_hilera = _Mapa()
                        inv_plants_mapa.set(hilera, mapa_pl_hilera)
                    mapa_pl_hilera.set(posicion, planta

                    )

                elif tag == "dron" and elem.attrib.get("hilera") is not None:

                    id_str = elem.attrib.get("id")
                    hilera = int(elem.attrib.get("hilera"))
                    try:
                        idnum = int(id_str)
                    except:
                        idnum = id_str
                    dr = drones_global.get(idnum)
                    if dr is not None:

                        inv_asignaciones.set(hilera, dr)

                elif tag == "plan":
                    nombre_plan = elem.attrib.get("nombre")
                    texto = (elem.text or "").strip()

                    pasos = ListaSimple()
                    
                    token = ""
                    i = 0
                    n = len(texto)
                    while i < n:
                        c = texto[i]
                        if c == ",":
                            s = token.strip()
                            if s:
                                self._agregar_paso_desde_str(pasos, s)
                            token = ""
                        else:
                            token += c
                        i += 1
                    s = token.strip()
                    if s:
                        self._agregar_paso_desde_str(pasos, s)

                    inv_planes.append(PlanRiego(nombre_plan, pasos))

                elif tag == "invernadero":

                    from ..tda.Mapa import Mapa as _Mapa
                    hileras_mapa = _Mapa()

                    for par in inv_plants_mapa:
                        hileras_mapa.set(par.k, Hilera(par.k, par.v))


                    asignaciones_mapa = _Mapa()
                    for par in inv_asignaciones:
                        original = par.v
                        clon = Dron(original.id, original.nombre)
                        clon.hilera = par.k
                        asignaciones_mapa.set(par.k, clon)

                    inv = Invernadero(inv_nombre, inv_num_h, inv_px_h, hileras_mapa, asignaciones_mapa, inv_planes)
                    invernaderos_lista.append(inv)


                    inv_nombre = None
                    inv_num_h = None
                    inv_px_h = None
                    inv_hileras = None
                    inv_asignaciones = None
                    inv_planes = None
                    inv_plants_mapa = None


        self.sistema.drones_global = drones_global
        self.sistema.invernaderos = invernaderos_lista

    def _agregar_paso_desde_str(self, pasos_lista, s):
      
        i = 0
        n = len(s)

        while i < n and s[i] == ' ':
            i += 1
        if i < n and (s[i] == 'H' or s[i] == 'h'):
            i += 1

        num_h = 0
        while i < n and s[i].isdigit():
            num_h = num_h * 10 + (ord(s[i]) - 48)
            i += 1

        while i < n and s[i] in ' -':
            if s[i] == '-':
                i += 1
                break
            i += 1

        while i < n and s[i] == ' ':
            i += 1
        if i < n and (s[i] == 'P' or s[i] == 'p'):
            i += 1
        num_p = 0
        while i < n and s[i].isdigit():
            num_p = num_p * 10 + (ord(s[i]) - 48)
            i += 1
        pasos_lista.append(PasoPlan(num_h, num_p))
