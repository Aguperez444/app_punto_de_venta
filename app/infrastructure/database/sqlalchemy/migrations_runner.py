from __future__ import annotations

import logging
from pathlib import Path

from app.infrastructure.database.sqlalchemy.engine_factory import _normalize_db_url

logger = logging.getLogger(__name__)


def _find_project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "alembic.ini").exists():
            return parent
    return Path(__file__).resolve().parents[4]


def run_alembic_upgrade(db_url: str) -> tuple[bool, str]:
    """Ejecuta `alembic upgrade head` de forma segura apuntando a `db_url`."""
    try:
        from alembic import command
        from alembic.config import Config

        normalized_url = _normalize_db_url(db_url)
        project_root = _find_project_root()
        alembic_ini = project_root / "alembic.ini"

        cfg = Config(str(alembic_ini))
        cfg.set_main_option("script_location", str(project_root / "migrations"))
        # Pasar la URL por attributes evita fallos de configparser si la clave contiene '%'
        cfg.attributes["db_url"] = normalized_url

        command.upgrade(cfg, "head")
        logger.info("Esquema de base de datos verificado/migrado correctamente.")
        return True, "Migraciones aplicadas correctamente."
    except Exception as exc:
        logger.exception("Error al ejecutar migraciones Alembic")
        return False, f"Error al ejecutar migraciones: {exc}"
