import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from core.Simulador import Simulador

class ReporteHTML:
    def __init__(self, templates_dir):
        self._templates = templates_dir

    def generar_por_invernadero(self, flask_app_unused, inv, out_dir):
       
        os.makedirs(out_dir, exist_ok=True)

       
        class Rwrap:
            def __init__(self, ti, tl, tg, tlm, pd):
                self.tiempo = ti
                self.total_litros = tl
                self.total_gramos = tg
                self.timeline = tlm
                self.por_dron = pd

        nombres = []
        resultados = []
        for plan in getattr(inv, "_planes"):
            sim = Simulador().simular_invernadero_plan(inv, plan)
            nombres.append(plan.nombre())
            resultados.append(Rwrap(sim.tiempo, sim.total_litros, sim.total_gramos, sim.timeline, sim.por_dron))

        class ResAcceso:
            def __init__(self, names, arr):
                self._n = names
                self._a = arr
            def __getitem__(self, key):
                i = 0
                while i < len(self._n):
                    if self._n[i] == key:
                        return self._a[i]
                    i += 1
                return None

        env = Environment(
            loader=FileSystemLoader(self._templates),
            autoescape=select_autoescape()
        )
        template = env.get_template("report.html")
        html = template.render(inv=inv, planes=getattr(inv, "_planes"), res=ResAcceso(nombres, resultados))

        ruta = os.path.join(out_dir, f"Reporte_{inv.nombre().replace(' ','_')}.html")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        return ruta

