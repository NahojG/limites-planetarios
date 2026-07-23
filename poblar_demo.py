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
    parser.add_argument("-n", type=int, default=40, help="estudiantes por semestre (por defecto 40)")
    parser.add_argument("-s", "--semestres", type=int, default=5, help="cantidad de semestres (por defecto 5)")
    parser.add_argument("--seed", type=int, default=None, help="semilla aleatoria (opcional)")
    parser.add_argument("--url", default=None, help="cadena de conexión (si DATABASE_URL no está en el entorno)")
    args = parser.parse_args()

    _exigir_base(args.url)

    print(f"Poblando la base con {args.semestres} semestres de {args.n} estudiantes ficticios…")
    res = demo.poblar_varios(semestres=args.semestres, n=args.n, seed=args.seed)
    for d in res["detalle"]:
        print(f"  {d['semestre']}: {d['prueba1']} con Prueba 1 · {d['prueba2']} con Prueba 2")
    print("Listo. Entra al panel y abre «Ver estadísticas» para visualizarlas.")


if __name__ == "__main__":
    main()
