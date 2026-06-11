#!/usr/bin/env python3
"""Lee desde consola el registro de visitas (visitas.jsonl).

Uso:
    python ver_visitas.py            # resumen + últimas 10 visitas
    python ver_visitas.py -n 50      # últimas 50 visitas
    python ver_visitas.py --todas    # todas las visitas, una por línea
    python ver_visitas.py --json     # exporta todo como un arreglo JSON

La ruta del archivo se toma de la variable de entorno RUTA_VISITAS
(por defecto "visitas.jsonl").
"""
import argparse
import json
import os
import sys
from collections import Counter

RUTA = os.environ.get("RUTA_VISITAS", "visitas.jsonl")


def cargar():
    if not os.path.exists(RUTA):
        print(f"Aún no hay archivo de visitas en: {RUTA}", file=sys.stderr)
        sys.exit(1)
    registros = []
    with open(RUTA, encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                registros.append(json.loads(linea))
    return registros


def resumen(registros):
    print(f"Total de visitas: {len(registros)}")
    if not registros:
        return
    print(f"Primera: {registros[0]['fecha']}")
    print(f"Última:  {registros[-1]['fecha']}")
    print(f"IPs únicas: {len({r.get('ip') for r in registros})}")

    rutas = Counter(r.get("ruta") for r in registros)
    print("\nRutas más visitadas:")
    for ruta, n in rutas.most_common(5):
        print(f"  {n:>4}  {ruta}")


def mostrar(registros):
    for r in registros:
        print(
            f"{r.get('fecha','?'):>20}  {r.get('ip',''):<15}  "
            f"{r.get('ruta',''):<12}  {r.get('navegador','')[:60]}"
        )


def main():
    parser = argparse.ArgumentParser(description="Lector de visitas.")
    parser.add_argument("-n", type=int, default=10, help="cuántas visitas mostrar")
    parser.add_argument("--todas", action="store_true", help="mostrar todas")
    parser.add_argument("--json", action="store_true", help="exportar como arreglo JSON")
    args = parser.parse_args()

    registros = cargar()

    if args.json:
        print(json.dumps(registros, ensure_ascii=False, indent=2))
        return

    resumen(registros)
    seleccion = registros if args.todas else registros[-args.n :]
    print(f"\nÚltimas {len(seleccion)} visitas:")
    mostrar(seleccion)


if __name__ == "__main__":
    main()
