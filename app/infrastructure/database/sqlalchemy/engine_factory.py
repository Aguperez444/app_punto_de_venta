from __future__ import annotations
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence

_DEFAULT_KWARGS = dict(
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,      # 30 min
    echo=True,
    isolation_level="READ COMMITTED",
)

def create_db_engine(db_url: Optional[str] = None, **overrides) -> Engine:
    """
    Crea y retorna un Engine de SQLAlchemy con la configuración estándar del proyecto.
    - db_url: si no se pasa, la toma de ConfigFilesPersistence.
    - overrides: permite ajustar parámetros (p. ej. echo=False en tests).
    """
    if db_url is None:
        config = ConfigFilesPersistence()
        db_url = str(config.get_ruta_bdd())


    kwargs = {**_DEFAULT_KWARGS, **overrides}
    return create_engine(db_url, **kwargs)