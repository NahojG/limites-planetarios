"""Capa de datos (PostgreSQL) de Guardianes del Holoceno.

Guarda el registro de estudiantes y los resultados de las dos pruebas del
semestre (inicio y fin del curso), para que la profesora pueda comparar cómo
estaba el planeta antes y después y socializar las estadísticas.

La conexión se toma de la variable de entorno DATABASE_URL, que Railway inyecta
automáticamente al vincular el servicio de PostgreSQL. Si la variable no existe
(por ejemplo en un arranque local sin base), la capa queda "no disponible" y la
aplicación sigue funcionando en modo de juego libre y anónimo.

Modelo:
  semestre(id, nombre, activo, prueba_activa)   -- prueba_activa: 0=cerrado, 1, 2
  estudiante(semestre_id, correo, nombre, sexo, edad, programa)
  resultado(semestre_id, correo, prueba, desenlace, salud, bienestar,
            niveles JSONB, decisiones JSONB)
"""
import os

try:
    import psycopg
    from psycopg.rows import dict_row
    from psycopg.types.json import Jsonb
except ImportError:  # psycopg aún no instalado (p. ej. entorno local mínimo)
    psycopg = None


def _url():
    url = os.environ.get("DATABASE_URL", "")
    # Algunos proveedores usan el esquema antiguo "postgres://"; psycopg 3
    # espera "postgresql://".
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    return url


def disponible():
    """True si hay librería y cadena de conexión: la persistencia está activa."""
    return psycopg is not None and bool(_url())


def _conectar():
    return psycopg.connect(_url(), row_factory=dict_row)


ESQUEMA = """
CREATE TABLE IF NOT EXISTS semestre (
    id            BIGSERIAL PRIMARY KEY,
    nombre        TEXT NOT NULL,
    activo        BOOLEAN NOT NULL DEFAULT TRUE,
    prueba_activa SMALLINT NOT NULL DEFAULT 0,
    creado        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS estudiante (
    id          BIGSERIAL PRIMARY KEY,
    semestre_id BIGINT NOT NULL REFERENCES semestre(id) ON DELETE CASCADE,
    correo      TEXT NOT NULL,
    nombre      TEXT,
    sexo        TEXT,
    edad        INTEGER,
    programa    TEXT,
    creado      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (semestre_id, correo)
);

CREATE TABLE IF NOT EXISTS resultado (
    id              BIGSERIAL PRIMARY KEY,
    semestre_id     BIGINT NOT NULL REFERENCES semestre(id) ON DELETE CASCADE,
    correo          TEXT NOT NULL,
    prueba          SMALLINT NOT NULL,
    fecha           TIMESTAMPTZ NOT NULL DEFAULT now(),
    desenlace       TEXT,
    salud_final     INTEGER,
    bienestar_final INTEGER,
    niveles         JSONB,
    decisiones      JSONB,
    UNIQUE (semestre_id, correo, prueba)
);
"""


def init_db():
    """Crea las tablas si no existen. Idempotente; seguro llamarlo al arrancar."""
    if not disponible():
        return
    with _conectar() as conn:
        conn.execute(ESQUEMA)


# --- Semestres ---------------------------------------------------------------

def semestre_activo():
    """Devuelve el semestre activo (dict) o None si no hay ninguno."""
    if not disponible():
        return None
    with _conectar() as conn:
        fila = conn.execute(
            "SELECT * FROM semestre WHERE activo ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return fila


def crear_semestre(nombre):
    """Archiva el semestre activo (si lo hay) y crea uno nuevo activo."""
    if not disponible():
        return None
    with _conectar() as conn:
        conn.execute("UPDATE semestre SET activo = FALSE, prueba_activa = 0 WHERE activo")
        fila = conn.execute(
            "INSERT INTO semestre (nombre, activo, prueba_activa) "
            "VALUES (%s, TRUE, 0) RETURNING *",
            (nombre,),
        ).fetchone()
    return fila


def set_prueba_activa(prueba):
    """Fija la prueba activa (0=cerrado, 1, 2) del semestre activo."""
    if not disponible():
        return
    with _conectar() as conn:
        conn.execute(
            "UPDATE semestre SET prueba_activa = %s WHERE activo",
            (int(prueba),),
        )


# --- Estudiantes y resultados ------------------------------------------------

def upsert_estudiante(semestre_id, correo, nombre=None, sexo=None, edad=None, programa=None):
    """Registra o actualiza los datos demográficos del estudiante."""
    if not disponible():
        return
    with _conectar() as conn:
        conn.execute(
            """
            INSERT INTO estudiante (semestre_id, correo, nombre, sexo, edad, programa)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (semestre_id, correo) DO UPDATE SET
                nombre   = COALESCE(EXCLUDED.nombre, estudiante.nombre),
                sexo     = COALESCE(EXCLUDED.sexo, estudiante.sexo),
                edad     = COALESCE(EXCLUDED.edad, estudiante.edad),
                programa = COALESCE(EXCLUDED.programa, estudiante.programa)
            """,
            (semestre_id, correo, nombre, sexo, edad, programa),
        )


def guardar_resultado(semestre_id, correo, prueba, snapshot):
    """Guarda (o reemplaza) el resultado de una prueba a partir de un snapshot
    de motor.snapshot_final(). Si el estudiante repite la misma prueba, se
    conserva el intento más reciente."""
    if not disponible():
        return
    with _conectar() as conn:
        conn.execute(
            """
            INSERT INTO resultado
                (semestre_id, correo, prueba, desenlace, salud_final,
                 bienestar_final, niveles, decisiones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (semestre_id, correo, prueba) DO UPDATE SET
                fecha           = now(),
                desenlace       = EXCLUDED.desenlace,
                salud_final     = EXCLUDED.salud_final,
                bienestar_final = EXCLUDED.bienestar_final,
                niveles         = EXCLUDED.niveles,
                decisiones      = EXCLUDED.decisiones
            """,
            (
                semestre_id,
                correo,
                int(prueba),
                snapshot.get("desenlace"),
                snapshot.get("salud_final"),
                snapshot.get("bienestar_final"),
                Jsonb(snapshot.get("niveles")),
                Jsonb(snapshot.get("decisiones")),
            ),
        )


def get_resultado(semestre_id, correo, prueba):
    """Devuelve el resultado de una prueba concreta (dict) o None."""
    if not disponible():
        return None
    with _conectar() as conn:
        return conn.execute(
            "SELECT * FROM resultado "
            "WHERE semestre_id = %s AND correo = %s AND prueba = %s",
            (semestre_id, correo, int(prueba)),
        ).fetchone()


def insertar_estudiantes_lote(semestre_id, estudiantes):
    """Inserta muchos estudiantes en una sola conexión (para datos de demo)."""
    if not disponible() or not estudiantes:
        return
    filas = [
        (semestre_id, e["correo"], e.get("nombre"), e.get("sexo"), e.get("edad"), e.get("programa"))
        for e in estudiantes
    ]
    with _conectar() as conn:
        conn.cursor().executemany(
            "INSERT INTO estudiante (semestre_id, correo, nombre, sexo, edad, programa) "
            "VALUES (%s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (semestre_id, correo) DO NOTHING",
            filas,
        )


def insertar_resultados_lote(semestre_id, resultados):
    """Inserta muchos resultados en una sola conexión (para datos de demo).

    Cada elemento: {'correo', 'prueba', 'snapshot'} con el snapshot del motor.
    """
    if not disponible() or not resultados:
        return
    filas = [
        (
            semestre_id, r["correo"], int(r["prueba"]),
            r["snapshot"].get("desenlace"), r["snapshot"].get("salud_final"),
            r["snapshot"].get("bienestar_final"),
            Jsonb(r["snapshot"].get("niveles")), Jsonb(r["snapshot"].get("decisiones")),
        )
        for r in resultados
    ]
    with _conectar() as conn:
        conn.cursor().executemany(
            "INSERT INTO resultado "
            "(semestre_id, correo, prueba, desenlace, salud_final, bienestar_final, niveles, decisiones) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (semestre_id, correo, prueba) DO NOTHING",
            filas,
        )


def borrar_todo():
    """Vacía por completo las tablas (semestres, estudiantes y resultados).

    Pensado para limpiar datos de demostración. Es irreversible.
    """
    if not disponible():
        return
    with _conectar() as conn:
        conn.execute("TRUNCATE resultado, estudiante, semestre RESTART IDENTITY CASCADE")


def conteos_semestre(semestre_id):
    """Resumen de participación del semestre para el panel de la profesora."""
    vacio = {"estudiantes": 0, "prueba1": 0, "prueba2": 0, "ambas": 0}
    if not disponible() or semestre_id is None:
        return vacio
    with _conectar() as conn:
        estudiantes = conn.execute(
            "SELECT count(*) AS n FROM estudiante WHERE semestre_id = %s",
            (semestre_id,),
        ).fetchone()["n"]
        por_prueba = conn.execute(
            "SELECT prueba, count(*) AS n FROM resultado "
            "WHERE semestre_id = %s GROUP BY prueba",
            (semestre_id,),
        ).fetchall()
        ambas = conn.execute(
            """
            SELECT count(*) AS n FROM (
                SELECT correo FROM resultado
                WHERE semestre_id = %s AND prueba IN (1, 2)
                GROUP BY correo HAVING count(DISTINCT prueba) = 2
            ) t
            """,
            (semestre_id,),
        ).fetchone()["n"]
    conteo = dict(vacio)
    conteo["estudiantes"] = estudiantes
    for fila in por_prueba:
        conteo["prueba1" if fila["prueba"] == 1 else "prueba2"] = fila["n"]
    conteo["ambas"] = ambas
    return conteo


def resumen_por_semestre():
    """Una fila por semestre (orden cronológico) con promedios de cada prueba.

    Sirve para la vista de evolución entre semestres.
    """
    if not disponible():
        return []
    with _conectar() as conn:
        return conn.execute(
            """
            SELECT
                s.id, s.nombre,
                count(r.*) FILTER (WHERE r.prueba = 1)              AS n1,
                count(r.*) FILTER (WHERE r.prueba = 2)              AS n2,
                avg(r.salud_final) FILTER (WHERE r.prueba = 1)      AS salud1,
                avg(r.salud_final) FILTER (WHERE r.prueba = 2)      AS salud2,
                avg(r.bienestar_final) FILTER (WHERE r.prueba = 1)  AS bienestar1,
                avg(r.bienestar_final) FILTER (WHERE r.prueba = 2)  AS bienestar2
            FROM semestre s
            LEFT JOIN resultado r ON r.semestre_id = s.id
            GROUP BY s.id, s.nombre
            ORDER BY s.id
            """
        ).fetchall()


def resultados_prueba(semestre_id, prueba):
    """Todos los resultados de una prueba del semestre (lista de dicts)."""
    if not disponible() or semestre_id is None:
        return []
    with _conectar() as conn:
        return conn.execute(
            "SELECT r.*, e.sexo, e.edad, e.programa "
            "FROM resultado r "
            "LEFT JOIN estudiante e "
            "  ON e.semestre_id = r.semestre_id AND e.correo = r.correo "
            "WHERE r.semestre_id = %s AND r.prueba = %s "
            "ORDER BY r.fecha",
            (semestre_id, int(prueba)),
        ).fetchall()


def pares_ambas_pruebas(semestre_id):
    """Estudiantes con Prueba 1 y 2, como lista de (resultado1, resultado2)."""
    if not disponible() or semestre_id is None:
        return []
    with _conectar() as conn:
        filas = conn.execute(
            """
            SELECT
                r1.correo AS correo,
                r1.desenlace AS d1, r1.salud_final AS s1,
                r1.bienestar_final AS b1, r1.niveles AS n1, r1.decisiones AS dec1,
                r2.desenlace AS d2, r2.salud_final AS s2,
                r2.bienestar_final AS b2, r2.niveles AS n2, r2.decisiones AS dec2
            FROM resultado r1
            JOIN resultado r2
              ON r1.semestre_id = r2.semestre_id AND r1.correo = r2.correo
            WHERE r1.semestre_id = %s AND r1.prueba = 1 AND r2.prueba = 2
            ORDER BY r1.correo
            """,
            (semestre_id,),
        ).fetchall()
    return filas
