from __future__ import annotations

import os
from typing import Optional

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine

from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence

_POSTGRES_DEFAULT_KWARGS = dict(
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
    isolation_level="READ COMMITTED",
)


def _normalize_db_url(raw_url: str) -> str:
    cleaned = raw_url.strip()
    if not cleaned:
        raise ValueError("La URL de la base de datos no está configurada.")
    # Si el usuario eligió una ruta de archivo .db/.sqlite sin prefijo de esquema
    if "://" not in cleaned and (
        cleaned.endswith(".db") or cleaned.endswith(".sqlite") or cleaned.endswith(".sqlite3")
    ):
        return f"sqlite:///{cleaned}"
    return cleaned


def create_db_engine(db_url: Optional[str] = None, **overrides) -> Engine:
    """
    Crea y retorna un Engine de SQLAlchemy adaptado al dialecto (PostgreSQL o SQLite).
    - db_url: si no se pasa, la toma de DATABASE_URL o ConfigFilesPersistence.
    - overrides: permite ajustar parámetros (p. ej. echo=True).
    """
    if db_url is None:
        config = ConfigFilesPersistence()
        db_url = config.get_ruta_bdd()

    normalized_url = _normalize_db_url(str(db_url))
    echo_default = os.getenv("SQL_ECHO", "0").lower() in ("1", "true", "yes")

    is_sqlite = normalized_url.startswith("sqlite:")
    if is_sqlite:
        kwargs = {"echo": echo_default, **overrides}
    else:
        kwargs = {**_POSTGRES_DEFAULT_KWARGS, "echo": echo_default, **overrides}

    engine = create_engine(normalized_url, **kwargs)

    if is_sqlite:

        @event.listens_for(engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, _connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def test_db_connection(db_url: str, timeout_seconds: int = 5) -> tuple[bool, str]:
    """Valida conectividad contra una URL SQLAlchemy ejecutando SELECT 1."""
    engine: Engine | None = None
    try:
        normalized = _normalize_db_url(db_url)
        connect_args = {}
        if normalized.startswith("postgresql"):
            connect_args["connect_timeout"] = timeout_seconds
        engine = create_db_engine(normalized, connect_args=connect_args)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Conexión exitosa a la base de datos."
    except Exception as exc:
        return False, f"Error de conexión: {exc}"
    finally:
        if engine is not None:
            engine.dispose()
