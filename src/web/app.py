
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, send_file
from ..core.Sistema import Sistema
from werkzeug.utils import secure_filename
from ..io.ParserXML import ParserXML
from ..core.Simulador import Simulador
from ..io.WriterXML import WriterXML
from ..reports.ReporteHTML import ReporteHTML
from ..viz.TDAGraphRenderer import TDAGraphRenderer
from ..tda.ListaSimple import ListaSimple


sistema = Sistema()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "ipc2_p2_mac_safari"
app.logger.setLevel('INFO')

app.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=0,
    TEMPLATES_AUTO_RELOAD=True
)

@app.after_request
def no_cache(resp):
    resp.headers["Cache-Control"] = "no-store, max-age=0"
    return resp

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR  = os.path.join(BASE_DIR, "out")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR,  exist_ok=True)

@app.route("/", methods=["GET"])
def index():

    invs = sistema.invernaderos if sistema.invernaderos is not None else ListaSimple()

    
    ultimo = app.config.get("__ULTIMO_RESULTADO__")

    
    ultimo_vm = None
    if ultimo:
        inv = ultimo["inv"]
        res = ultimo["resultado"]

       
        dron_columns = []
        asign_rows = []
        for par in inv.asignaciones:           
            dron_columns.append(par.v.nombre)
            asign_rows.append({"hilera": par.k, "dron": par.v.nombre})

      
        efic_rows = []
        for par in res.por_dron:               
            efic_rows.append({
                "dron": par.k,
                "litros": getattr(par.v, "a", 0.0),
                "gramos": getattr(par.v, "b", 0.0),
            })

        timeline_rows = []
        for tick in res.timeline:               
            acciones = {}
            for acc in tick.acciones:          
                acciones[acc.dron_nombre] = acc.accion
            timeline_rows.append({"segundos": tick.segundos, "acciones": acciones})

        ultimo_vm = {
            "inv_nombre": inv.nombre,
            "plan_nombre": ultimo["plan_nombre"],
            "tiempo_optimo": res.tiempo_optimo,
            "agua_total": res.agua_total,
            "fert_total": res.fert_total,
            "dron_columns": dron_columns,
            "asign_rows": asign_rows,
            "efic_rows": efic_rows,
            "timeline_rows": timeline_rows,
        }

    return render_template("index.html",
                           invernaderos=invs,
                           ultimo=ultimo,     
                           ultimo_vm=ultimo_vm)  


@app.route("/cargar", methods=["POST"])
def cargar():
 
    app.logger.info("POST /cargar keys=%s form=%s", list(request.files.keys()), dict(request.form))

    file = (
        request.files.get("archivo")
        or request.files.get("file")
        or request.files.get("config")
        or (next(iter(request.files.values()), None) if request.files else None)
    )

    if not file or file.filename.strip() == "":
        app.logger.warning("No se recibió archivo en request.files")
        flash("Selecciona un archivo XML.", "error")
        return redirect(url_for("index"))

    fname = secure_filename(file.filename)
    if not fname.lower().endswith(".xml"):
        flash("El archivo debe ser .xml", "error")
        return redirect(url_for("index"))


    xml_path = os.path.join(DATA_DIR, "entrada.xml")
    file.save(xml_path)
    app.logger.info("Archivo guardado en %s", xml_path)

    

    try:
        parser = ParserXML(sistema)  
        parser.cargar_desde_archivo(xml_path)  

       
        if getattr(sistema, "invernaderos", None) is None:
            sistema.invernaderos = ListaSimple()


        app.config["__ULTIMO_RESULTADO__"] = None

        flash("XML cargado correctamente.", "ok")
        try:
            os.system(f'''open -a "Safari" "{url_for('index', _external=True)}#entrada"''')
        except Exception:
            pass
        return redirect(url_for("index") + "#entrada")
    except Exception as e:
        app.logger.exception("Error al cargar/parsing XML")
        flash(f"Error al cargar/parsing XML: {e}", "error")
        return redirect(url_for("index"))


@app.route("/descargar/salida")
def descargar_salida():

    xml_path = os.path.join(OUT_DIR, "salida.xml")
    if not os.path.exists(xml_path):
        flash("Aún no hay salida.xml. Ejecute una simulación primero.", "error")
        return redirect(url_for("index"))
    return send_from_directory(OUT_DIR, "salida.xml", as_attachment=True)

@app.route("/simular", methods=["POST"])
def simular():
    inv_nombre = request.form.get("invernadero")
    plan_nombre = request.form.get("plan")

    if not inv_nombre or not plan_nombre:
        flash("Seleccione invernadero y plan.", "error")
        return redirect(url_for("index"))

    inv = sistema.obtener_invernadero(inv_nombre)
    if inv is None:
        flash("Invernadero no encontrado.", "error")
        return redirect(url_for("index"))


    pertenece = False
    for p in inv.planes:
        if p.nombre == plan_nombre:
            pertenece = True
            break
    if not pertenece:
        flash("El plan seleccionado no pertenece al invernadero elegido.", "error")
        return redirect(url_for("index"))

    try:
        sim = Simulador(sistema)
        resultado = sim.simular_plan(inv_nombre, plan_nombre)
    except Exception as e:
        app.logger.exception("Error en simulación")
        flash(f"Error en simulación: {e}", "error")
        return redirect(url_for("index"))


    from ..tda.Mapa import Mapa
    mp_plan = Mapa(); mp_plan.set(plan_nombre, resultado)
    mp_inv  = Mapa(); mp_inv.set(inv_nombre, mp_plan)

    try:
        WriterXML(sistema).escribir_salida(os.path.join(OUT_DIR, "salida.xml"), mp_inv)
    except Exception as e:
        app.logger.exception("Error al escribir salida.xml")
        flash(f"Advertencia: no se pudo escribir salida.xml: {e}", "error")

    try:
        ReporteHTML(OUT_DIR).generar_por_invernadero(inv, mp_plan)
    except Exception as e:
        app.logger.exception("Error al generar reporte HTML")
        flash(f"Advertencia: no se pudo generar el reporte HTML: {e}", "error")


    app.config["__ULTIMO_RESULTADO__"] = {
        "inv": inv,
        "plan_nombre": plan_nombre,
        "resultado": resultado
    }

    flash("Simulación completada.", "ok")

    return redirect(url_for("index") + "#resultados")

@app.route("/reporte/<inv_safe_name>")
def reporte(inv_safe_name):

    filename = f"Reporte_{inv_safe_name}.html"
    return send_from_directory(OUT_DIR, filename)

@app.route("/grafo-tda")
def grafo_tda():

    t = request.args.get("t", type=int, default=1)

    data = app.config.get("__ULTIMO_RESULTADO__")
    if not data:
        flash("Primero ejecute una simulación.", "error")
        return redirect(url_for("index"))

    inv = data["inv"]
    resultado = data["resultado"]
    plan_nombre = data["plan_nombre"]


    if t < 1:
        t = 1
    if t > resultado.tiempo_optimo:
        t = resultado.tiempo_optimo

    svg_path = TDAGraphRenderer(OUT_DIR).render_estado(inv, resultado, t, plan_nombre=plan_nombre)


    return send_file(svg_path, mimetype="image/svg+xml")

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")
