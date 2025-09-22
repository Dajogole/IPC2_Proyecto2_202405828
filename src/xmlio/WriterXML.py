import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from core.Simulador import Simulador

class WriterXML:
    def __init__(self, ruta_salida:str):
        self._ruta = ruta_salida
        os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)

    def escribir(self, invernaderos):
        root = ET.Element("datosSalida")
        li = ET.SubElement(root, "listaInvernaderos")
        for inv in invernaderos:
            xin = ET.SubElement(li, "invernadero")
            xin.set("nombre", inv.nombre())
            lp = ET.SubElement(xin, "listaPlanes")
            for plan in inv._planes:
                sim = Simulador().simular_invernadero_plan(inv, plan)
                xplan = ET.SubElement(lp, "plan")
                xplan.set("nombre", plan.nombre())
                ET.SubElement(xplan, "tiempoOptimoSegundos").text = str(sim.tiempo)
                ET.SubElement(xplan, "aguaRequeridaLitros").text = str(sim.total_litros)
                ET.SubElement(xplan, "fertilizanteRequeridoGramos").text = str(sim.total_gramos)
                ed = ET.SubElement(xplan, "eficienciaDronesRegadores")
                for s in sim.por_dron:
                    nombre,L,G = s.split("|")
                    xdr = ET.SubElement(ed, "dron")
                    xdr.set("nombre", nombre)
                    xdr.set("litrosAgua", str(L))
                    xdr.set("gramosFertilizante", str(G))
                xinstr = ET.SubElement(xplan, "instrucciones")
                for seg in sim.timeline:
                    xt = ET.SubElement(xinstr, "tiempo")
                    xt.set("segundos", str(seg.t))
                    for a in seg.acciones:
                        xd = ET.SubElement(xt, "dron")
                        xd.set("nombre", a.dron)
                        xd.set("accion", a.accion)

        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(self._ruta, "w", encoding="utf-8") as f:
            f.write(xml_str)
        return self._ruta

