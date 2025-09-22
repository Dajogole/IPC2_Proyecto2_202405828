import os
import shutil
from graphviz import Digraph

class TDAGraphRenderer:
    def __init__(self, out_dir="out"):
        self._out = out_dir
        os.makedirs(out_dir, exist_ok=True)
        self._asegurar_dot_en_path()

    def _asegurar_dot_en_path(self):
        
     
        if shutil.which("dot"):
            return

        candidatos = [
            "/opt/homebrew/bin/dot",   
            "/usr/local/bin/dot",      
            "/usr/bin/dot",           
            r"C:\Program Files\Graphviz\bin\dot.exe",  
        ]
        for ruta in candidatos:
            if os.path.exists(ruta) and os.access(ruta, os.X_OK):
                
                carpeta = os.path.dirname(ruta)
                os.environ["PATH"] = carpeta + (os.pathsep + os.environ.get("PATH", ""))
                return


        raise RuntimeError(
            "No se encontró el binario 'dot' de Graphviz.\n"
            "Instálalo y colócalo en el PATH. En macOS con Homebrew:\n"
            "  brew install graphviz\n"
            "Si usas Apple Silicon (M1/M2/M3), asegúrate que /opt/homebrew/bin esté en tu PATH:\n"
            "  echo 'export PATH=\"/opt/homebrew/bin:$PATH\"' >> ~/.zshrc && source ~/.zshrc\n"
        )

    def graficar_estado(self, inv, resultado, t, nombre_archivo="tda_estado"):
        g = Digraph("TDAEstado")
        g.attr(rankdir="LR", fontsize="10")

     
        g.node("Drones", "Drones (lista)")
        for dr in inv.drones():
            g.node(f"DR_{dr.nombre()}", f"{dr.nombre()} (H{dr.hilera()})\npos={dr.pos()}\nL={dr.litros():.1f} G={dr.gramos():.0f}")
            g.edge("Drones", f"DR_{dr.nombre()}")

       
        g.node("Timeline", "Timeline (lista)")
        prev_node = None
        for seg in resultado.timeline:
            if seg.t > t:
                break
            cur_node = f"S{seg.t}"
            g.node(cur_node, f"t={seg.t}")
            if prev_node is None:
                g.edge("Timeline", cur_node)
            else:
                g.edge(prev_node, cur_node)
            prev_node = cur_node

           
            for a in seg.acciones:
                an = f"A{seg.t}_{a.dron}"
                g.node(an, f"{a.dron}: {a.accion}")
                g.edge(cur_node, an)

        ruta_gv = os.path.join(self._out, f"{nombre_archivo}.gv")
        g.save(ruta_gv)
        g.render(filename=nombre_archivo, directory=self._out, format="png", cleanup=True)
        return os.path.join(self._out, f"{nombre_archivo}.png")
