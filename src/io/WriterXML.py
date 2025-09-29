from ..tda.ListaSimple import ListaSimple
from ..tda.Mapa import Mapa
from ..domain import InstruccionesTiempo

class WriterXML:
    def __init__(self, sistema):
        self.sistema = sistema

    def escribir_salida(self, ruta_xml_out: str, resultados_por_invernadero):


        s = []
        s.append("<?xml version=\"1.0\"?>\n")
        s.append("<datosSalida>\n")
        s.append("  <listaInvernaderos>\n")

        for par_inv in resultados_por_invernadero:
            inv_nombre = par_inv.k
            s.append("    <invernadero nombre='{}'>\n".format(self._esc(inv_nombre)))
            s.append("      <listaPlanes>\n")
            mapa_planes = par_inv.v
            for par_plan in mapa_planes:
                plan_nombre = par_plan.k
                res = par_plan.v
                s.append("        <plan nombre='{}'>\n".format(self._esc(plan_nombre)))
                s.append("          <tiempoOptimoSegundos> {} </tiempoOptimoSegundos>\n".format(int(res.tiempo_optimo)))
                s.append("          <aguaRequeridaLitros> {} </aguaRequeridaLitros>\n".format(self._fmt_num(res.agua_total)))
                s.append("          <fertilizanteRequeridoGramos> {} </fertilizanteRequeridoGramos>\n".format(self._fmt_num(res.fert_total)))
                s.append("          <eficienciaDronesRegadores>\n")

                for par_d in res.por_dron:
                    s.append("            <dron nombre='{}' litrosAgua={} gramosFertilizante={}/>\n".format(
                        self._esc(par_d.k),
                        self._fmt_num(par_d.v.a),
                        self._fmt_num(par_d.v.b)
                    ))
                s.append("          </eficienciaDronesRegadores>\n")
                s.append("          <instrucciones>\n")

                for it in res.timeline:
                    s.append("            <tiempo segundos={}> \n".format(int(it.segundos)))
                    for acc in it.acciones:
                        s.append("              <dron nombre='{}' accion='{}'/>\n".format(self._esc(acc.dron_nombre), self._esc(acc.accion)))
                    s.append("            </tiempo>\n")
                s.append("          </instrucciones>\n")
                s.append("        </plan>\n")
            s.append("      </listaPlanes>\n")
            s.append("    </invernadero>\n")
        s.append("  </listaInvernaderos>\n")
        s.append("</datosSalida>\n")

        with open(ruta_xml_out, "w", encoding="utf-8") as f:
            f.write("".join(s))

    def _esc(self, txt):
        if txt is None:
            return ""
        return str(txt).replace("&", "&amp;").replace("'", "&apos;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

    def _fmt_num(self, x):
        if int(x) == float(x):
            return str(int(x))
        return str(float(x))
