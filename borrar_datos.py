#!/usr/bin/env python3
"""Borra TODOS los datos de la base (semestres, estudiantes y resultados).

Pensado para limpiar los datos de demostración. Es irreversible.

Uso:
    export DATABASE_URL="postgresql://usuario:clave@host:puerto/base"
    python borrar_datos.py         # pide confirmación
    python borrar_datos.py --si    # borra sin preguntar

En Railway:  railway run python borrar_datos.py
"""
import argparse
import sys

from game import db


def main():
    parser = argparse.ArgumentParser(description="Borra todos los datos de la base.")
    parser.add_argument("--si", action="store_true", help="borra sin pedir confirmación")
    args = parser.parse_args()

    if not db.disponible():
        print("No hay DATABASE_URL configurada: no hay base que borrar.", file=sys.stderr)
        sys.exit(1)

    if not args.si:
        print("Esto BORRARÁ todos los semestres, estudiantes y resultados. No se puede deshacer.")
        respuesta = input("Escribe BORRAR para confirmar: ").strip()
        if respuesta != "BORRAR":
            print("Cancelado. No se borró nada.")
            sys.exit(0)

    db.borrar_todo()
    print("Base vaciada por completo.")


if __name__ == "__main__":
    main()
