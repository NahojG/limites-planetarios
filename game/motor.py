"""Motor del juego Guardianes del Holoceno.

El estado del juego vive en la sesión de Flask como un dict serializable.
Cada límite se mide en una escala 0-100 de transgresión:
  0-32  zona segura  |  33-65 zona de riesgo  |  66-100 zona de alto riesgo
"""
import json
import os

_DATA = os.path.join(os.path.dirname(__file__), "data")


def _cargar(nombre):
    with open(os.path.join(_DATA, nombre), encoding="utf-8") as f:
        return json.load(f)


LIMITES = _cargar("limites.json")
CARTAS = _cargar("cartas.json")
QUIZ = _cargar("quiz.json")

# Secuencia de turnos: dilemas intercalados con preguntas de quiz.
# Cada turno avanza 5 años desde 2025.
SECUENCIA = [
    ("dilema", 0), ("dilema", 1), ("dilema", 2),
    ("quiz", 0),
    ("dilema", 3), ("dilema", 4), ("dilema", 5),
    ("quiz", 1),
    ("dilema", 6), ("dilema", 7),
    ("quiz", 2),
    ("dilema", 8), ("dilema", 9),
]

ANIO_INICIAL = 2025
ANIOS_POR_TURNO = 5

# Etiquetas de los desenlaces para mostrarlos en el servidor (comparativo,
# panel, estadísticas). Deben coincidir con las de static/js/juego.js.
DESENLACES = {
    "guardian": "🌱 Guardiana/Guardián del Holoceno",
    "equilibrista": "🌍 Equilibrista planetario",
    "al_borde": "⚠️ Al borde del abismo",
    "herencia_rota": "🔥 Una herencia rota",
    "colapso_planetario": "💀 Colapso planetario",
    "colapso_social": "🏚️ Colapso social",
}


def etiqueta_desenlace(clave):
    return DESENLACES.get(clave, "—")


def nuevo_juego():
    return {
        "turno": 0,
        "niveles": {clave: datos["inicial"] for clave, datos in LIMITES.items()},
        "bienestar": 55,
        "terminado": False,
        "resultado": None,
        # Historial de las decisiones de gobernanza (solo dilemas), en orden.
        # Es la base del comparativo entre la Prueba 1 y la Prueba 2.
        "decisiones": [],
    }


def _zona(nivel):
    if nivel < 33:
        return "segura"
    if nivel < 66:
        return "riesgo"
    return "alto"


def _promedio(niveles):
    return sum(niveles.values()) / len(niveles)


def salud_planetaria(estado):
    return round(100 - _promedio(estado["niveles"]))


def _turno_actual(estado):
    if estado["turno"] >= len(SECUENCIA):
        return None
    return SECUENCIA[estado["turno"]]


def estado_publico(estado):
    """Versión del estado que se envía al navegador (sin respuestas del quiz)."""
    publico = {
        "turno": estado["turno"],
        "total_turnos": len(SECUENCIA),
        "anio": ANIO_INICIAL + estado["turno"] * ANIOS_POR_TURNO,
        "bienestar": estado["bienestar"],
        "salud": salud_planetaria(estado),
        "terminado": estado["terminado"],
        "resultado": estado["resultado"],
        "limites": [
            {
                "clave": clave,
                "nombre": LIMITES[clave]["nombre"],
                "corto": LIMITES[clave]["corto"],
                "descripcion": LIMITES[clave]["descripcion"],
                "referencia": LIMITES[clave]["referencia"],
                "nivel": round(nivel),
                "zona": _zona(nivel),
            }
            for clave, nivel in estado["niveles"].items()
        ],
    }
    turno = _turno_actual(estado)
    if turno and not estado["terminado"]:
        tipo, indice = turno
        if tipo == "dilema":
            carta = CARTAS[indice]
            publico["tarjeta"] = {
                "tipo": "dilema",
                "titulo": carta["titulo"],
                "contexto": carta["contexto"],
                "opciones": [op["texto"] for op in carta["opciones"]],
            }
        else:
            pregunta = QUIZ[indice]
            publico["tarjeta"] = {
                "tipo": "quiz",
                "titulo": "Pausa de saberes",
                "contexto": pregunta["pregunta"],
                "opciones": pregunta["opciones"],
            }
    return publico


def _aplicar_efectos(estado, efectos, bienestar):
    for clave, delta in efectos.items():
        nivel = estado["niveles"][clave] + delta
        estado["niveles"][clave] = max(0, min(100, nivel))
    estado["bienestar"] = max(0, min(100, estado["bienestar"] + bienestar))


def _evaluar_fin(estado):
    """Colapsos anticipados y resultado final al agotar los turnos."""
    niveles = estado["niveles"]
    promedio = _promedio(niveles)
    criticos = sum(1 for n in niveles.values() if n >= 90)

    # La degradación ecológica erosiona el bienestar: sequías, desastres,
    # desplazamientos. No hay bienestar duradero fuera de la zona segura. Cuanto
    # más se degrada el planeta, más fuerte cae el bienestar, de modo que un
    # desplome ecológico sostenido puede arrastrar a un colapso social.
    if promedio >= 52:
        estado["bienestar"] = max(0, estado["bienestar"] - (1 + round((promedio - 52) / 2)))

    if estado["bienestar"] <= 0:
        estado["terminado"] = True
        estado["resultado"] = "colapso_social"
        return
    if promedio >= 70 or criticos >= 3:
        estado["terminado"] = True
        estado["resultado"] = "colapso_planetario"
        return
    if estado["turno"] >= len(SECUENCIA):
        estado["terminado"] = True
        seguros = sum(1 for n in niveles.values() if n < 33)
        if promedio < 42 and estado["bienestar"] >= 50:
            estado["resultado"] = "guardian"
        elif promedio < 52:
            estado["resultado"] = "equilibrista"
        elif promedio < 64:
            estado["resultado"] = "al_borde"
        else:
            estado["resultado"] = "herencia_rota"
        estado["seguros"] = seguros


def snapshot_final(estado):
    """Resumen persistible de una partida terminada (para guardar en la base)."""
    return {
        "desenlace": estado.get("resultado"),
        "salud_final": salud_planetaria(estado),
        "bienestar_final": estado.get("bienestar"),
        "niveles": {clave: round(nivel) for clave, nivel in estado["niveles"].items()},
        "decisiones": estado.get("decisiones", []),
    }


def jugar_turno(estado, opcion):
    """Aplica la opción elegida para el turno actual. Devuelve el feedback."""
    turno = _turno_actual(estado)
    if turno is None or estado["terminado"]:
        return None

    tipo, indice = turno
    respuesta = {"tipo": tipo}

    if tipo == "dilema":
        carta = CARTAS[indice]
        if not 0 <= opcion < len(carta["opciones"]):
            return None
        elegida = carta["opciones"][opcion]
        _aplicar_efectos(estado, elegida["efectos"], elegida["bienestar"])
        respuesta["feedback"] = elegida["feedback"]
        respuesta["efectos"] = elegida["efectos"]
        respuesta["bienestar"] = elegida["bienestar"]
        # Registramos la decisión para poder comparar pruebas más adelante.
        estado.setdefault("decisiones", []).append({
            "indice": indice,
            "titulo": carta["titulo"],
            "opcion": opcion,
            "texto": elegida["texto"],
        })
    else:
        pregunta = QUIZ[indice]
        if not 0 <= opcion < len(pregunta["opciones"]):
            return None
        acierto = opcion == pregunta["correcta"]
        respuesta["acierto"] = acierto
        respuesta["correcta"] = pregunta["opciones"][pregunta["correcta"]]
        respuesta["feedback"] = pregunta["explicacion"]
        if acierto:
            # El conocimiento sana: alivia los dos límites más transgredidos.
            peores = sorted(estado["niveles"], key=estado["niveles"].get)[-2:]
            efectos = {clave: -4 for clave in peores}
            _aplicar_efectos(estado, efectos, 2)
            respuesta["efectos"] = efectos
            respuesta["bienestar"] = 2

    estado["turno"] += 1
    _evaluar_fin(estado)
    return respuesta
