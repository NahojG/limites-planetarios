#!/usr/bin/env python3
"""Puebla la base con datos ficticios para VER las estadísticas.

Nota: lo más fácil es usar el botón «Cargar datos de demostración» del panel
docente (corre dentro de la app desplegada, sin instalar nada ni configurar la
URL). Este script es la alternativa por línea de comandos.

Uso:
    export DATABASE_URL="postgresql://usuario:clave@host:puerto/base"
    python poblar_demo.py                 # 40 estudiantes, semestre "DEMO"
    python poblar_demo.py -n 80           # 80 estudiantes
    python poblar_demo.py --url "postgresql://..."   # si no hay DATABASE_URL
"""
import argparse
import os
import sys

from game import db, demo


def _exigir_base(url_cli):
    if url_cli:
        os.environ["DATABASE_URL"] = url_cli
    if db.psycopg is None:
        print("Falta la librería psycopg. Instala las dependencias:\n"
              "    pip install -r requirements.txt\n"
              "(si usas `railway run`, el script corre en tu máquina, no en Railway).",
              file=sys.stderr)
        sys.exit(1)
    if not os.environ.get("DATABASE_URL"):
        print("No hay DATABASE_URL. Pásala con --url \"$DATABASE_URL\" o la cadena completa.",
              file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Puebla la base con datos de demostración.")
    parser.add_argument("-n", type=int, default=40, help="cantidad de estudiantes (por defecto 40)")
    parser.add_argument("--semestre", default="DEMO", help="nombre del semestre (por defecto DEMO)")
    parser.add_argument("--seed", type=int, default=None, help="semilla aleatoria (opcional)")
    parser.add_argument("--url", default=None, help="cadena de conexión (si DATABASE_URL no está en el entorno)")
    args = parser.parse_args()

    _exigir_base(args.url)

    print(f"Poblando la base con {args.n} estudiantes ficticios…")
    res = demo.poblar(n=args.n, nombre=args.semestre, seed=args.seed)
    print(f"Listo: semestre «{res['semestre']}» · {res['prueba1']} con Prueba 1 · "
          f"{res['prueba2']} con Prueba 2.")
    print("Entra al panel y abre «Ver estadísticas» para visualizarlas.")


if __name__ == "__main__":
    main()
