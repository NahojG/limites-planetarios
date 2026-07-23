"""Guardianes del Holoceno — juego educativo sobre límites planetarios.

Evaluación Módulo 4, Cátedra Ambiental, Universidad de Antioquia.
Estudiante: Johan Granados Vega · Profesora: Cristina López-Gallego
"""
import os
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from game import db, demo, motor, stats, visitas

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "holoceno-dev")

# Contraseña única de la profesora para el panel y las estadísticas.
PROFESOR_PASSWORD = os.environ.get("PROFESOR_PASSWORD", "")

# Crea las tablas si hay base de datos configurada (DATABASE_URL). Si no,
# la app funciona igual en modo de juego libre y anónimo.
try:
    db.init_db()
except Exception:  # pragma: no cover - la app no debe caer por la base
    pass


@app.before_request
def registrar_visita():
    # Solo registramos páginas reales, no estáticos ni llamadas internas de la API.
    if request.path.startswith(("/static", "/api")):
        return
    try:
        visitas.registrar(request)
    except OSError:
        # Si falla la escritura (p. ej. disco de solo lectura) no rompemos la app.
        pass


def _prueba_en_curso():
    """Semestre activo con una prueba abierta (1 o 2), o None.

    Cuando devuelve un semestre, la actividad está "abierta" por la profesora y
    el juego pide registro y guarda resultados. Cuando es None, el juego es de
    acceso libre y anónimo (comportamiento por defecto de la web pública).
    """
    sem = db.semestre_activo()
    if sem and sem["prueba_activa"] in (1, 2):
        return sem
    return None


def _estudiante_valido(sem):
    """Datos del estudiante en sesión si corresponden al semestre activo."""
    est = session.get("estudiante")
    if est and sem and est.get("semestre_id") == sem["id"]:
        return est
    return None


@app.get("/")
def inicio():
    return render_template("inicio.html")


@app.get("/jugar")
def jugar():
    sem = _prueba_en_curso()
    if sem and not _estudiante_valido(sem):
        # Hay una prueba abierta y el estudiante aún no se ha registrado.
        return redirect(url_for("registro"))
    if "estado" not in session:
        session["estado"] = motor.nuevo_juego()
    return render_template("juego.html")


@app.get("/registro")
def registro():
    sem = _prueba_en_curso()
    if not sem:
        # No hay prueba abierta: no se registra, se juega libremente.
        return redirect(url_for("jugar"))
    return render_template("registro.html", semestre=sem)


@app.post("/registro")
def registro_enviar():
    sem = _prueba_en_curso()
    if not sem:
        return redirect(url_for("jugar"))

    correo = (request.form.get("correo") or "").strip().lower()
    # El correo es el único campo obligatorio (y debe parecer un correo).
    if "@" not in correo or "." not in correo.split("@")[-1]:
        return render_template("registro.html", semestre=sem, error=True), 400

    nombre = (request.form.get("nombre") or "").strip() or None
    sexo = (request.form.get("sexo") or "").strip() or None
    programa = (request.form.get("programa") or "").strip() or None
    edad_txt = (request.form.get("edad") or "").strip()
    edad = int(edad_txt) if edad_txt.isdigit() else None

    try:
        db.upsert_estudiante(sem["id"], correo, nombre, sexo, edad, programa)
    except Exception:
        pass

    session["estudiante"] = {
        "semestre_id": sem["id"],
        "correo": correo,
        "prueba": sem["prueba_activa"],
    }
    session["estado"] = motor.nuevo_juego()
    return redirect(url_for("jugar"))


@app.get("/comparativo")
def comparativo():
    sem = db.semestre_activo()
    est = session.get("estudiante")
    if not (sem and est and est.get("semestre_id") == sem["id"]):
        return redirect(url_for("jugar"))
    r1 = db.get_resultado(sem["id"], est["correo"], 1)
    r2 = db.get_resultado(sem["id"], est["correo"], 2)
    if not (r1 and r2):
        # Todavía no existen las dos mediciones para comparar.
        return redirect(url_for("jugar"))

    limites = [
        {"clave": clave, "nombre": datos["nombre"], "corto": datos["corto"]}
        for clave, datos in motor.LIMITES.items()
    ]
    # Degradación del planeta a partir de la salud (igual que en el juego:
    # 0 = sano con salud >= 70, 1 = colapso con salud <= 28).
    def _deg(salud):
        return round(max(0.0, min(1.0, (70 - (salud or 0)) / 42)), 3)
    # Decisiones que cambiaron entre la Prueba 1 y la Prueba 2.
    cambios = []
    for d1, d2 in zip(r1["decisiones"], r2["decisiones"]):
        if d1.get("opcion") != d2.get("opcion"):
            cambios.append({"titulo": d1.get("titulo"), "antes": d1.get("texto"), "despues": d2.get("texto")})

    return render_template(
        "comparativo.html",
        r1=r1,
        r2=r2,
        limites=limites,
        cambios=cambios,
        etiqueta=motor.etiqueta_desenlace,
        deg1=_deg(r1["salud_final"]),
        deg2=_deg(r2["salud_final"]),
    )


@app.post("/nueva-partida")
def nueva_partida():
    session["estado"] = motor.nuevo_juego()
    return redirect(url_for("jugar"))


@app.get("/api/estado")
def api_estado():
    estado = session.get("estado")
    if estado is None:
        estado = motor.nuevo_juego()
        session["estado"] = estado
    return jsonify(motor.estado_publico(estado))


@app.post("/api/decidir")
def api_decidir():
    estado = session.get("estado")
    if estado is None:
        return jsonify({"error": "No hay partida activa"}), 400
    datos = request.get_json(silent=True) or {}
    opcion = datos.get("opcion")
    if not isinstance(opcion, int):
        return jsonify({"error": "Opción inválida"}), 400
    respuesta = motor.jugar_turno(estado, opcion)
    if respuesta is None:
        return jsonify({"error": "Turno inválido"}), 400
    session["estado"] = estado

    if estado["terminado"]:
        respuesta.update(_guardar_si_corresponde(estado))

    return jsonify({"respuesta": respuesta, "estado": motor.estado_publico(estado)})


def _guardar_si_corresponde(estado):
    """Persiste el resultado si el juego terminó dentro de una prueba abierta.

    Devuelve pistas para el cliente: si se guardó y si el estudiante ya puede
    ver el comparativo (solo en la Prueba 2, cuando existe su Prueba 1).
    """
    sem = _prueba_en_curso()
    est = _estudiante_valido(sem)
    if not est:
        return {}
    prueba = est["prueba"]
    try:
        db.guardar_resultado(sem["id"], est["correo"], prueba, motor.snapshot_final(estado))
        comparativo = prueba == 2 and db.get_resultado(sem["id"], est["correo"], 1) is not None
    except Exception:
        return {}
    return {"guardado": True, "prueba": prueba, "comparativo": bool(comparativo)}


# ---------------------------------------------------------------------------
# Panel de la profesora (protegido por contraseña)
# ---------------------------------------------------------------------------

def requiere_profesor(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("profesor"):
            return redirect(url_for("panel"))
        return vista(*args, **kwargs)
    return envoltura


@app.get("/panel")
def panel():
    if not session.get("profesor"):
        return render_template("login.html")
    sem = db.semestre_activo()
    conteos = db.conteos_semestre(sem["id"]) if sem else db.conteos_semestre(None)
    return render_template(
        "panel.html",
        disponible=db.disponible(),
        semestre=sem,
        conteos=conteos,
    )


@app.post("/panel/login")
def panel_login():
    clave = request.form.get("clave") or ""
    if PROFESOR_PASSWORD and clave == PROFESOR_PASSWORD:
        session["profesor"] = True
        return redirect(url_for("panel"))
    return render_template("login.html", error=True), 401


@app.post("/panel/salir")
def panel_salir():
    session.pop("profesor", None)
    return redirect(url_for("panel"))


@app.get("/estadisticas")
@requiere_profesor
def estadisticas():
    sem = db.semestre_activo()
    if not sem:
        return render_template("estadisticas.html", semestre=None, datos=None)
    rows1 = db.resultados_prueba(sem["id"], 1)
    rows2 = db.resultados_prueba(sem["id"], 2)
    pares = db.pares_ambas_pruebas(sem["id"])
    datos = {
        "prueba1": stats.agregados_prueba(rows1),
        "prueba2": stats.agregados_prueba(rows2),
        "comparacion": stats.comparacion(pares),
        "participacion": db.conteos_semestre(sem["id"]),
    }
    return render_template("estadisticas.html", semestre=sem, datos=datos)


@app.post("/panel/semestre")
@requiere_profesor
def panel_semestre():
    nombre = (request.form.get("nombre") or "").strip()
    if nombre:
        db.crear_semestre(nombre)
    return redirect(url_for("panel"))


@app.post("/panel/prueba")
@requiere_profesor
def panel_prueba():
    valor = request.form.get("prueba")
    if valor in ("0", "1", "2") and db.semestre_activo():
        db.set_prueba_activa(int(valor))
    return redirect(url_for("panel"))


@app.post("/panel/demo/poblar")
@requiere_profesor
def panel_demo_poblar():
    if db.disponible():
        demo.poblar(n=40, nombre="DEMO")
    return redirect(url_for("estadisticas"))


@app.post("/panel/demo/borrar")
@requiere_profesor
def panel_demo_borrar():
    if db.disponible():
        db.borrar_todo()
    return redirect(url_for("panel"))


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
