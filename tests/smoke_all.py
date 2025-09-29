
import os
from src.core.Sistema import Sistema
from src.io.ParserXML import ParserXML
from src.core.Simulador import Simulador
from src.io.WriterXML import WriterXML
from src.tda.Mapa import Mapa

BASE = os.path.dirname(__file__)
RAIZ = os.path.abspath(os.path.join(BASE, ".."))
DATA = os.path.join(RAIZ, "data", "entrada.xml")
OUT = os.path.join(RAIZ, "out")
os.makedirs(OUT, exist_ok=True)

sis = Sistema()
ParserXML(sis).cargar_desde_archivo(DATA)


inv = None
if sis.invernaderos is not None:
    for x in sis.invernaderos:
        inv = x
        break

plan_nombre = None
if inv is not None:
    for p in inv.planes:
        plan_nombre = p.nombre
        break

if inv is None or plan_nombre is None:
    raise SystemExit("No hay datos en data/entrada.xml")

res = Simulador(sis).simular_plan(inv.nombre, plan_nombre)
mp_plan = Mapa()
mp_plan.set(plan_nombre, res)
mp_inv = Mapa()
mp_inv.set(inv.nombre, mp_plan)

WriterXML(sis).escribir_salida(os.path.join(OUT, "salida.xml"), mp_inv)
print("OK. salida.xml generado.")
