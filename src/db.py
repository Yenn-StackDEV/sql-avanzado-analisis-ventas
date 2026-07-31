import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
SEED_PATH = BASE_DIR / "sql" / "seed.sql"


def get_connection() -> sqlite3.Connection:
    """Crea una conexion a una base de datos SQLite en memoria."""
    conexion = sqlite3.connect(":memory:")
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion


def inicializar_base_datos(conexion: sqlite3.Connection) -> None:
    """Crea las tablas y carga los datos ficticios de ejemplo."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as archivo_schema:
        conexion.executescript(archivo_schema.read())

    with open(SEED_PATH, "r", encoding="utf-8") as archivo_seed:
        conexion.executescript(archivo_seed.read())

    conexion.commit()
