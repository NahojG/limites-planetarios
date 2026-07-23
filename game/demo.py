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


def poblar(n=40, nombre="DEMO", seed=None):
    """Crea un semestre de demostración con `n` estudiantes ficticios.

    Devuelve un resumen: {'semestre', 'n', 'prueba1', 'prueba2'}.
    """
    rng = random.Random(seed)
    db.init_db()
    sem = db.crear_semestre(nombre)
    sid = sem["id"]

    n1 = n2 = 0
    for i in range(n):
        correo = f"demo{i:03d}@ejemplo.edu.co"
        db.upsert_estudiante(
            sid, correo,
            nombre=f"Estudiante {i:03d}",
            sexo=rng.choice(SEXOS),
            edad=rng.randint(16, 34),
            programa=rng.choice(PROGRAMAS),
        )
        db.set_prueba_activa(1)
        sesgo1 = rng.uniform(0.0, 0.15) if rng.random() < 0.2 else rng.uniform(0.15, 0.55)
        db.guardar_resultado(sid, correo, 1, simular(sesgo1, rng))
        n1 += 1
        if rng.random() < 0.8:
            db.set_prueba_activa(2)
            db.guardar_resultado(sid, correo, 2, simular(rng.uniform(0.45, 0.95), rng))
            n2 += 1

    db.set_prueba_activa(0)  # deja la actividad cerrada
    return {"semestre": nombre, "n": n, "prueba1": n1, "prueba2": n2}
