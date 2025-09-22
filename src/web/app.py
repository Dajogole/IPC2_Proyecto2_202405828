import os
from flask import Flask, request, render_template, redirect, url_for, send_file, flash
from xmlio.ParserXML import ParserXML
from xmlio.WriterXML import WriterXML
from core.Simulador import Simulador
from reports.ReporteHTML import ReporteHTML
from viz.TDAGraphRenderer import TDAGraphRenderer

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "ipc2-p2"

class Estado:
    def __init__(self):
        from tda.Lista import ListaEnlazada
        self.invernaderos = None
        self.ultimo_inv = None
        self.ultimo_plan = None
        self.ultimo_resultado = None
E = Estado()

@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="POST":
        f = request.files.get("archivo")
        if not f:
            flash("Sube un XML válido")
            return redirect(url_for("home"))
        os.makedirs("data", exist_ok=True)
        path = os.path.join("data","entrada.xml")
        f.save(path)
        px = ParserXML(path).parse()
        E.invernaderos = px.invernaderos()
        flash("Configuración cargada")
        return redirect(url_for("simular"))
    return render_template("home.html")

@app.route("/simular", methods=["GET","POST"])
def simular():
    if E.invernaderos is None:
        flash("Carga primero un XML")
        return redirect(url_for("home"))

    inv_sel = request.form.get("inv") if request.method=="POST" else None
    plan_sel = request.form.get("plan") if request.method=="POST" else None

    inv = E.invernaderos.get(0)
    if inv_sel:
        for iv in E.invernaderos:
            if iv.nombre()==inv_sel:
                inv = iv
    plan = inv._planes.get(0)
    if plan_sel:
        for pl in inv._planes:
            if pl.nombre()==plan_sel:
                plan = pl

    if request.method=="POST" and request.form.get("accion")=="run":
        res = Simulador().simular_invernadero_plan(inv, plan)
        E.ultimo_inv = inv
        E.ultimo_plan = plan
        E.ultimo_resultado = res
        flash("Simulación completada")
        return redirect(url_for("simular"))

    inv_names = ""
    for iv in E.invernaderos:
        inv_names += iv.nombre() + "\n"
    plan_names = ""
    for pl in inv._planes:
        plan_names += pl.nombre() + "\n"

    return render_template("simular.html",
                           inv=inv,
                           inv_names=inv_names.strip().split("\n"),
                           plan=plan,
                           plan_names=plan_names.strip().split("\n"),
                           res=E.ultimo_resultado)

@app.route("/descargar/salida.xml")
def descargar_xml():
    if E.invernaderos is None:
        flash("No hay datos")
        return redirect(url_for("home"))
    ruta = WriterXML("out/salida.xml").escribir(E.invernaderos)
    return send_file(ruta, as_attachment=True)

@app.route("/reporte")
def reporte():
    if E.invernaderos is None:
        flash("No hay datos")
        return redirect(url_for("home"))
    inv = E.invernaderos.get(0) if E.ultimo_inv is None else E.ultimo_inv
    rep = ReporteHTML("src/reports/templates").generar_por_invernadero(app, inv, "out")
    return send_file(rep, as_attachment=False)

@app.route("/grafo-tda", methods=["GET","POST"])
def grafo_tda():
    if E.ultimo_inv is None or E.ultimo_resultado is None:
        flash("Ejecuta una simulación primero")
        return redirect(url_for("simular"))
    t = int(request.form.get("t") or "1")
    png = TDAGraphRenderer().graficar_estado(E.ultimo_inv, E.ultimo_resultado, t, "estado_t")
    return send_file(png, as_attachment=False)

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")

