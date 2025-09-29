from ..tda.ListaSimple import ListaSimple
from ..tda.Mapa import Mapa
import os

class ReporteHTML:
    def __init__(self, out_dir: str):
        self.out_dir = out_dir

    def generar_por_invernadero(self, invernadero, resultados_por_plan):
        # resultados_por_plan: Mapa plan_nombre -> ResultadoPlan
        # Generar un archivo por invernadero
        file_path = os.path.join(self.out_dir, "Reporte_{}.html".format(self._safe_name(invernadero.nombre)))
        html = []
        html.append("<!doctype html><html><head><meta charset='utf-8'><title>Reporte {}</title>".format(self._esc(invernadero.nombre)))
        html.append("<style>body{font-family: -apple-system, Helvetica, Arial; padding:20px;} table{border-collapse:collapse;margin:10px 0;} th,td{border:1px solid #ccc;padding:6px 10px;} h2{margin-top:28px;} code{background:#f2f2f2;padding:2px 4px;border-radius:4px;}</style>")
        html.append("</head><body>")
        html.append("<h1>Reporte Invernadero: {}</h1>".format(self._esc(invernadero.nombre)))

        # Tabla Asignación de drones a hileras
        html.append("<h2>Asignación de Drones a Hileras</h2><table><tr><th>Hilera</th><th>Dron</th></tr>")
        for par in invernadero.asignaciones:
            html.append("<tr><td>H{}</td><td>{}</td></tr>".format(par.k, self._esc(par.v.nombre)))
        html.append("</table>")

        for par_plan in resultados_por_plan:
            plan_nombre = par_plan.k
            res = par_plan.v
            html.append("<h2>Plan: {}</h2>".format(self._esc(plan_nombre)))
            html.append("<p><b>Tiempo óptimo:</b> {} s &nbsp; | &nbsp; <b>Agua total:</b> {} L &nbsp; | &nbsp; <b>Fertilizante total:</b> {} g</p>".format(int(res.tiempo_optimo), self._fmt_num(res.agua_total), self._fmt_num(res.fert_total)))

            # Eficiencia por dron
            html.append("<h3>Eficiencia por Dron</h3><table><tr><th>Dron</th><th>Litros</th><th>Gramos</th></tr>")
            for par_d in res.por_dron:
                html.append("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                    self._esc(par_d.k), self._fmt_num(par_d.v.a), self._fmt_num(par_d.v.b)))
            html.append("</table>")

            # Cronograma por tiempo
            html.append("<h3>Instrucciones por Tiempo</h3>")
            # Encabezados: Tiempo + dron por columna (ordenar por nombre de dron según aparezcan)
            # Para no usar listas, imprimimos por filas y buscamos las acciones del dron en tiempo t recorriendo el mapa de drones
            # Construiremos un encabezado con los nombres de los drones en asignación:
            html.append("<table><tr><th>Tiempo (s)</th>")
            # Es coherente mostrar por asignaciones (garantiza un orden estable por hilera)
            for par_asig in invernadero.asignaciones:
                html.append("<th>{}</th>".format(self._esc(par_asig.v.nombre)))
            html.append("</tr>")

            # Por cada tiempo, desplegar acciones de cada dron en orden de asignaciones
            for it in res.timeline:
                html.append("<tr><td>{}</td>".format(int(it.segundos)))
                for par_asig in invernadero.asignaciones:
                    # Buscar acción de este dron en este tiempo (recorrer acciones del tiempo)
                    acc_txt = ""
                    for acc in it.acciones:
                        if acc.dron_nombre == par_asig.v.nombre:
                            acc_txt = acc.accion
                            break
                    html.append("<td>{}</td>".format(self._esc(acc_txt)))
                html.append("</tr>")
            html.append("</table>")

        html.append("</body></html>")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("".join(html))
        return file_path

    def _esc(self, txt):
        if txt is None: return ""
        return str(txt).replace("&", "&amp;").replace("<","&lt;").replace(">","&gt;")

    def _safe_name(self, name):
        return "".join(ch if ch.isalnum() else "_" for ch in name)

    def _fmt_num(self, x):
        if int(x) == float(x):
            return str(int(x))
        return str(float(x))
