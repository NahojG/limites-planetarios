"""Agregaciones para la pestaña de estadísticas de la profesora.

Recibe filas de resultados (dicts, ya con niveles/decisiones decodificados desde
JSONB) y devuelve estructuras listas para graficar. No toca la base de datos:
app.py obtiene las filas con game.db y se las pasa a estas funciones.

Todo es agregado: nunca se exponen correos ni filas individuales.
"""
from game import motor

LIMITES_ORDEN = list(motor.LIMITES.keys())
LIMITES_NOMBRES = [motor.LIMITES[c]["corto"] for c in LIMITES_ORDEN]
DESENLACES_ORDEN = list(motor.DESENLACES.keys())
# Etiquetas cortas para los ejes de las gráficas (las completas no caben).
DESENLACES_CORTOS_MAPA = {
    "guardian": "🌱 Guardián",
    "equilibrista": "🌍 Equilibrista",
    "al_borde": "⚠️ Al borde",
    "herencia_rota": "🔥 Herencia rota",
    "colapso_planetario": "💀 Colapso planet.",
    "colapso_social": "🏚️ Colapso social",
}
DESENLACES_NOMBRES = [DESENLACES_CORTOS_MAPA[c] for c in DESENLACES_ORDEN]

# Cubetas de edad para la demografía.
_EDAD_CUBETAS = [
    ("≤17", lambda e: e <= 17),
    ("18–20", lambda e: 18 <= e <= 20),
    ("21–23", lambda e: 21 <= e <= 23),
    ("24–26", lambda e: 24 <= e <= 26),
    ("27+", lambda e: e >= 27),
]


def _promedio(valores):
    valores = [v for v in valores if v is not None]
    return round(sum(valores) / len(valores), 1) if valores else 0


def _conteo_desenlaces(rows):
    conteo = {clave: 0 for clave in DESENLACES_ORDEN}
    for r in rows:
        if r.get("desenlace") in conteo:
            conteo[r["desenlace"]] += 1
    return [conteo[c] for c in DESENLACES_ORDEN]


def _limites_promedio(rows):
    prom = []
    for clave in LIMITES_ORDEN:
        prom.append(_promedio([r["niveles"].get(clave) for r in rows if r.get("niveles")]))
    return prom


def _demografia(rows):
    sexo, programa, edad = {}, {}, {et: 0 for et, _ in _EDAD_CUBETAS}
    for r in rows:
        s = r.get("sexo") or "Sin dato"
        sexo[s] = sexo.get(s, 0) + 1
        p = r.get("programa") or "Sin dato"
        programa[p] = programa.get(p, 0) + 1
        e = r.get("edad")
        if e is not None:
            for etiqueta, prueba in _EDAD_CUBETAS:
                if prueba(e):
                    edad[etiqueta] += 1
                    break
    # Programa: los 6 más frecuentes, el resto agrupado en "Otros".
    prog_ord = sorted(programa.items(), key=lambda kv: kv[1], reverse=True)
    if len(prog_ord) > 6:
        principales = prog_ord[:6]
        otros = sum(n for _, n in prog_ord[6:])
        prog_ord = principales + [("Otros", otros)]
    return {
        "sexo": {"etiquetas": list(sexo.keys()), "valores": list(sexo.values())},
        "programa": {"etiquetas": [k for k, _ in prog_ord], "valores": [n for _, n in prog_ord]},
        "edad": {"etiquetas": list(edad.keys()), "valores": list(edad.values())},
    }


def agregados_prueba(rows):
    """Resumen de una prueba (Prueba 1 o Prueba 2)."""
    return {
        "n": len(rows),
        "salud_prom": _promedio([r.get("salud_final") for r in rows]),
        "bienestar_prom": _promedio([r.get("bienestar_final") for r in rows]),
        "desenlaces": {"etiquetas": DESENLACES_NOMBRES, "valores": _conteo_desenlaces(rows)},
        "limites": {"etiquetas": LIMITES_NOMBRES, "valores": _limites_promedio(rows)},
        "demografia": _demografia(rows),
    }


def comparacion(pares):
    """Compara Prueba 1 y Prueba 2 para quienes hicieron ambas.

    `pares` son filas de db.pares_ambas_pruebas (con columnas s1/b1/n1/dec1 y
    s2/b2/n2/dec2).
    """
    n = len(pares)
    d_salud = _promedio([p["s2"] - p["s1"] for p in pares]) if n else 0
    d_bien = _promedio([p["b2"] - p["b1"] for p in pares]) if n else 0

    des1 = {c: 0 for c in DESENLACES_ORDEN}
    des2 = {c: 0 for c in DESENLACES_ORDEN}
    for p in pares:
        if p["d1"] in des1:
            des1[p["d1"]] += 1
        if p["d2"] in des2:
            des2[p["d2"]] += 1

    lim1, lim2 = [], []
    for clave in LIMITES_ORDEN:
        lim1.append(_promedio([p["n1"].get(clave) for p in pares if p.get("n1")]))
        lim2.append(_promedio([p["n2"].get(clave) for p in pares if p.get("n2")]))

    # Decisiones que más cambió el grupo, por dilema.
    cambios = {}
    for p in pares:
        for a, b in zip(p.get("dec1") or [], p.get("dec2") or []):
            titulo = a.get("titulo")
            if titulo is None:
                continue
            cambios.setdefault(titulo, 0)
            if a.get("opcion") != b.get("opcion"):
                cambios[titulo] += 1
    cambios_ord = sorted(cambios.items(), key=lambda kv: kv[1], reverse=True)

    return {
        "n": n,
        "salud_delta": d_salud,
        "bienestar_delta": d_bien,
        "salud1_prom": _promedio([p["s1"] for p in pares]) if n else 0,
        "salud2_prom": _promedio([p["s2"] for p in pares]) if n else 0,
        "desenlaces": {
            "etiquetas": DESENLACES_NOMBRES,
            "prueba1": [des1[c] for c in DESENLACES_ORDEN],
            "prueba2": [des2[c] for c in DESENLACES_ORDEN],
        },
        "limites": {"etiquetas": LIMITES_NOMBRES, "prueba1": lim1, "prueba2": lim2},
        "decisiones": {
            "etiquetas": [t for t, _ in cambios_ord],
            "valores": [n for _, n in cambios_ord],
        },
    }
