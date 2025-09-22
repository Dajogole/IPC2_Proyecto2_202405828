from xmlio.ParserXML import ParserXML
from core.Simulador import Simulador
from xmlio.WriterXML import WriterXML
from viz.TDAGraphRenderer import TDAGraphRenderer
from flask import Flask
from reports.ReporteHTML import ReporteHTML

px = ParserXML("data/entrada_ejemplo.xml").parse()
inv = px.invernaderos().get(0)
plan = inv._planes.get(0)
res = Simulador().simular_invernadero_plan(inv, plan)
assert res.tiempo > 0
WriterXML("out/salida.xml").escribir(px.invernaderos())
TDAGraphRenderer().graficar_estado(inv, res, t=2, nombre_archivo="estado_test")
app = Flask(__name__, template_folder="src/reports/templates")
ReporteHTML("src/reports/templates").generar_por_invernadero(app, inv, "out")
print("OK")

