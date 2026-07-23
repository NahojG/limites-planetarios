"""Generación de datos de demostración para previsualizar las estadísticas.

Lo usan tanto el script `poblar_demo.py` como el botón del panel docente. Crea un
semestre con estudiantes ficticios que juegan la Prueba 1 (inicio) y, la mayoría,
la Prueba 2 (fin, con mejores decisiones), para que las tres pestañas de
estadísticas tengan contenido variado. Los datos son inventados.
"""
import random

from game import db, motor

PROGRAMAS = [
    "Estadística", "Biología", "Derecho", "Medicina", "Ingeniería Ambiental",
    "Historia", "Química", "Economía", "Trabajo Social", "Ciencias Políticas",
]
SEXOS = ["F", "M", "Otro", None]


def _puntaje_opcion(opcion):
    """Qué tan buena es una opción para el planeta y el bienestar (mayor = mejor)."""
    return -sum(opcion["efectos"].values()) + opcion["bienestar"]


def simular(sesgo, rng):
    """Juega una partida. `sesgo` en [0,1]: 0 decide mal, 1 decide bien.

    El jugador evalúa el efecto real de cada opción y, según su sesgo, elige la
    mejor, la peor o una al azar, para lograr un abanico de desenlaces.
    """
    estado = motor.nuevo_juego()
    for _ in range(len(motor.SECUENCIA)):
        if estado["terminado"]:
            break
        tipo, indice = motor.SECUENCIA[estado["turno"]]
        if tipo == "dilema":
            opciones = motor.CARTAS[indice]["opciones"]
            orden = sorted(range(len(opciones)), key=lambda i: _puntaje_opcion(opciones[i]))
            r = rng.random()
            if r < sesgo:
                opcion = orden[-1]
            elif r > 1 - (1 - sesgo) * 0.75:
                opcion = orden[0]
            else:
                opcion = rng.randrange(len(opciones))
        else:
            correcta = motor.QUIZ[indice]["correcta"]
            n = len(motor.QUIZ[indice]["opciones"])
            opcion = correcta if rng.random() < sesgo else rng.randrange(n)
        if motor.jugar_turno(estado, opcion) is None:
            break
    return motor.snapshot_final(estado)


def _un_semestre(nombre, n, rng, drift=0.0):
    """Genera (sin escribir en la base) los estudiantes y resultados de un semestre.

    `drift` en [0,1] sube un poco la habilidad de las cohortes más recientes, para
    que la evolución entre semestres muestre una leve mejora. Los correos incluyen
    el nombre del semestre: cada semestre son estudiantes distintos.
    """
    estudiantes, resultados = [], []
    n1 = n2 = 0
    for i in range(n):
        correo = f"demo{i:03d}@{nombre}.ejemplo.edu.co"
        estudiantes.append({
            "correo": correo,
            "nombre": f"Estudiante {i:03d}",
            "sexo": rng.choice(SEXOS),
            "edad": rng.randint(16, 34),
            "programa": rng.choice(PROGRAMAS),
        })
        sesgo1 = rng.uniform(0.0, 0.15) if rng.random() < 0.2 else rng.uniform(0.15, 0.5 + 0.1 * drift)
        resultados.append({"correo": correo, "prueba": 1, "snapshot": simular(sesgo1, rng)})
        n1 += 1
        if rng.random() < 0.8:
            sesgo2 = rng.uniform(0.45 + 0.2 * drift, min(0.98, 0.9 + 0.08 * drift))
            resultados.append({"correo": correo, "prueba": 2, "snapshot": simular(sesgo2, rng)})
            n2 += 1
    return estudiantes, resultados, n1, n2


def poblar(n=40, nombre="DEMO", seed=None, drift=0.0):
    """Crea un semestre de demostración con `n` estudiantes ficticios.

    Devuelve un resumen: {'semestre', 'n', 'prueba1', 'prueba2'}.
    """
    rng = random.Random(seed)
    db.init_db()
    sem = db.crear_semestre(nombre)
    estudiantes, resultados, n1, n2 = _un_semestre(nombre, n, rng, drift)
    db.insertar_estudiantes_lote(sem["id"], estudiantes)
    db.insertar_resultados_lote(sem["id"], resultados)
    db.set_prueba_activa(0)  # deja la actividad cerrada
    return {"semestre": nombre, "n": n, "prueba1": n1, "prueba2": n2}


def _nombres_semestres(k):
    """k nombres de semestre en orden cronológico, terminando en 2026-1."""
    anio, periodo, seq = 2026, 1, []
    for _ in range(k):
        seq.append(f"{anio}-{periodo}")
        if periodo == 1:
            periodo, anio = 2, anio - 1
        else:
            periodo = 1
    return list(reversed(seq))


def poblar_varios(semestres=5, n=40, seed=None):
    """Crea varios semestres de demostración (estudiantes distintos en cada uno).

    Las cohortes más recientes mejoran un poco, para que la vista «Entre
    semestres» muestre una evolución. Devuelve un resumen por semestre.
    """
    db.init_db()
    nombres = _nombres_semestres(semestres)
    detalle = []
    for i, nombre in enumerate(nombres):
        rng = random.Random(None if seed is None else seed + i)
        drift = i / (semestres - 1) if semestres > 1 else 1.0
        sem = db.crear_semestre(nombre)
        estudiantes, resultados, n1, n2 = _un_semestre(nombre, n, rng, drift)
        db.insertar_estudiantes_lote(sem["id"], estudiantes)
        db.insertar_resultados_lote(sem["id"], resultados)
        detalle.append({"semestre": nombre, "prueba1": n1, "prueba2": n2})
    db.set_prueba_activa(0)
    return {"semestres": len(nombres), "n": n, "detalle": detalle}
