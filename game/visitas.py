"""Registro sencillo de visitas en un archivo JSON Lines.

Cada visita se guarda como un objeto JSON por línea (formato JSONL), lo que
permite agregar registros de forma segura sin reescribir todo el archivo.

La ruta del archivo es configurable con la variable de entorno RUTA_VISITAS;
en Railway conviene apuntarla a un Volume montado para que no se borre en cada
redeploy (el disco es efímero).
"""
import json
import os
import threading
from datetime import datetime, timezone

RUTA = os.environ.get("RUTA_VISITAS", "visitas.jsonl")

_lock = threading.Lock()


def registrar(request):
    """Guarda los metadatos de una visita a partir de la petición Flask."""
    # Tras un proxy (Railway) la IP real viene en X-Forwarded-For.
    reenvio = request.headers.get("X-Forwarded-For", "")
    ip = reenvio.split(",")[0].strip() if reenvio else request.remote_addr

    registro = {
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ip": ip,
        "ruta": request.path,
        "navegador": request.headers.get("User-Agent", ""),
        "referente": request.headers.get("Referer", ""),
        "idioma": request.headers.get("Accept-Language", ""),
    }

    linea = json.dumps(registro, ensure_ascii=False)
    with _lock:
        with open(RUTA, "a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")
