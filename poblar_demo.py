#!/usr/bin/env python3
"""Puebla la base con datos ficticios para VER las estadísticas.

Crea un semestre de demostración con estudiantes que juegan la Prueba 1 (inicio)
y, la mayoría, también la Prueba 2 (fin, con mejores decisiones), de modo que las
tres pestañas de estadísticas tengan contenido variado.

Uso:
    export DATABASE_URL="postgresql://usuario:clave@host:puerto/base"
    python poblar_demo.py                 # 40 estudiantes, semestre "DEMO"
    python poblar_demo.py -n 80           # 80 estudiantes
    python poblar_demo.py --semestre 2026-2

En Railway puedes ejecutarlo con:  railway run python poblar_demo.py

Los datos son inventados y sirven solo para previsualizar la interfaz.
"""
import argparse
import random
import sys

from game import db, motor

PROGRAMAS = [
    "Estadística", "Biología", "Derecho", "Medicina", "Ingeniería Ambiental",
    "Historia", "Química", "Economía", "Trabajo Social", "Ciencias Políticas",
]
SEXOS = ["F", "M", "Otro", None]


def _puntaje_opcion(opcion):
    """Qué tan buena es una opción para el planeta y el bienestar (mayor = mejor)."""
    # efectos positivos = más transgresión (peor); por eso se restan.
    return -sum(opcion["efectos"].values()) + opcion["bienestar"]


def simular(sesgo, rng):
    """Juega una partida. `sesgo` en [0,1]: 0 decide mal, 1 decide bien.

    El jugador simulado evalúa el efecto real de cada opción y, según su sesgo,
    elige la mejor, la peor o una al azar. Así se logra un abanico de desenlaces
    (desde colapsos hasta Guardián) para que la demo muestre las seis barras.
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
                opcion = orden[-1]              # la mejor
            elif r > 1 - (1 - sesgo) * 0.75:
                opcion = orden[0]               # la peor
            else:
                opcion = rng.randrange(len(opciones))
        else:
            # En el quiz, el buen jugador acierta (y así "sana") con más frecuencia.
            correcta = motor.QUIZ[indice]["correcta"]
            n = len(motor.QUIZ[indice]["opciones"])
            opcion = correcta if rng.random() < sesgo else rng.randrange(n)
        if motor.jugar_turno(estado, opcion) is None:
            break
    return motor.snapshot_final(estado)


def main():
    parser = argparse.ArgumentParser(description="Puebla la base con datos de demostración.")
    parser.add_argument("-n", type=int, default=40, help="cantidad de estudiantes (por defecto 40)")
    parser.add_argument("--semestre", default="DEMO", help="nombre del semestre (por defecto DEMO)")
    parser.add_argument("--seed", type=int, default=None, help="semilla aleatoria (opcional)")
    args = parser.parse_args()

    if not db.disponible():
        print("No hay DATABASE_URL configurada: no se puede poblar la base.", file=sys.stderr)
        sys.exit(1)

    rng = random.Random(args.seed)
    db.init_db()
    sem = db.crear_semestre(args.semestre)
    sid = sem["id"]
    print(f"Semestre de demostración creado: «{sem['nombre']}» (id {sid})")

    n1 = n2 = 0
    for i in range(args.n):
        correo = f"demo{i:03d}@ejemplo.edu.co"
        db.upsert_estudiante(
            sid, correo,
            nombre=f"Estudiante {i:03d}",
            sexo=rng.choice(SEXOS),
            edad=rng.randint(16, 34),
            programa=rng.choice(PROGRAMAS),
        )
        # Prueba 1: al inicio del curso deciden peor (sesgo bajo); algunos muy mal.
        db.set_prueba_activa(1)
        sesgo1 = rng.uniform(0.0, 0.15) if rng.random() < 0.2 else rng.uniform(0.15, 0.55)
        db.guardar_resultado(sid, correo, 1, simular(sesgo1, rng))
        n1 += 1
        # ~80% también hacen la Prueba 2, decidiendo mejor (sesgo alto).
        if rng.random() < 0.8:
            db.set_prueba_activa(2)
            db.guardar_resultado(sid, correo, 2, simular(rng.uniform(0.45, 0.95), rng))
            n2 += 1

    db.set_prueba_activa(0)  # deja la actividad cerrada
    print(f"Listo: {args.n} estudiantes · {n1} con Prueba 1 · {n2} con Prueba 2.")
    print("Entra al panel y abre «Ver estadísticas» para visualizarlas.")


if __name__ == "__main__":
    main()
