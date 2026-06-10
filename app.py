"""Guardianes del Holoceno — juego educativo sobre límites planetarios.

Evaluación Módulo 4, Cátedra Ambiental, Universidad de Antioquia.
Estudiante: Johan Granados Vega · Profesora: Cristina López-Gallego
"""
import os

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from game import motor

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "holoceno-dev")


@app.get("/")
def inicio():
    return render_template("inicio.html")


@app.get("/jugar")
def jugar():
    if "estado" not in session:
        session["estado"] = motor.nuevo_juego()
    return render_template("juego.html")


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
    return jsonify({"respuesta": respuesta, "estado": motor.estado_publico(estado)})


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
