from graphviz import Digraph
import os

class TDAGraphRenderer:
    """
    Renderiza un diagrama de la SECUENCIA del plan:
    H#-P# -> H#-P# -> ... y resalta el paso irrigado más reciente al tiempo t.
    """
    def __init__(self, out_dir: str):
        self.out_dir = out_dir

    def _count_riegos_hasta_t(self, resultado_plan, t: int) -> int:
        """Cuenta cuántas acciones 'Regar' ocurrieron hasta el segundo t (inclusive)."""
        c = 0
        for tick in resultado_plan.timeline:

            if int(getattr(tick, "segundos", 0)) > int(t):
                break
            for acc in tick.acciones:
                if getattr(acc, "accion", "") == "Regar":
                    c += 1
        return c

    def _buscar_plan(self, invernadero, plan_nombre=None):
        """Busca un plan por nombre; si no se indica, devuelve el primero disponible."""
        if plan_nombre:
            for p in invernadero.planes:
                if p.nombre == plan_nombre:
                    return p

        for p in invernadero.planes:
            return p
        return None

    def render_estado(self, invernadero, resultado_plan, t: int, plan_nombre=None):
        """
        Genera un SVG con la secuencia completa de pasos del plan y resalta
        el paso irrigado que corresponde al estado en el segundo t.
        """
        plan = self._buscar_plan(invernadero, plan_nombre)
        if plan is None:
            raise RuntimeError("No se encontró un plan en el invernadero para graficar.")

        riegos = self._count_riegos_hasta_t(resultado_plan, t)
        idx_resaltado = riegos - 1 

        dot = Digraph(comment=f"Estado t={t}")
        dot.attr(rankdir="LR", bgcolor="white")
        dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica", fontsize="12")

        
        prev = None
        i = 0
        for paso in plan.pasos:
            label = f"H{paso.hilera}-P{paso.posicion}"
            fill = "#cfe8ff"      
            color = "#2b6cb0"
            if i == idx_resaltado:
                fill = "#7fb3ff"  
                color = "#1a365d"
            node_id = f"n{i}"
            dot.node(node_id, label, fillcolor=fill, color=color)
            if prev is not None:
                dot.edge(prev, node_id, color="#5a67d8", penwidth="1.6", arrowsize="0.8")
            prev = node_id
            i += 1


        dot.attr(label=f"t = {t}s  •  riegos completados: {max(riegos,0)}",
                 labelloc="t", fontsize="14", fontname="Helvetica-Bold", color="#2d3748")

        base = os.path.join(self.out_dir, f"tda_t{int(t)}")
        path = dot.render(filename=base, format="svg", cleanup=True)
        return path
