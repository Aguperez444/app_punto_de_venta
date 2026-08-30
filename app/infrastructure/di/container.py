from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.engine import Engine

from app.application.ports.clock import IClock
from app.application.ports.unit_of_work import UowFactory
from app.infrastructure.config.auth_service import AuthService
from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence
from app.infrastructure.database.sqlalchemy.migrations_runner import run_alembic_upgrade
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import (
    build_uow_factory,
    reset_uow_factory,
)
from app.infrastructure.time.system_clock import SystemClock


@dataclass
class AppContainer:
    """Composition Root central de la aplicación para inyección de dependencias."""

    config: ConfigFilesPersistence = field(default_factory=ConfigFilesPersistence)
    auth_service: AuthService = field(default_factory=AuthService)
    clock: IClock = field(default_factory=SystemClock)
    _uow_factory: UowFactory | None = field(default=None, init=False, repr=False)
    _engine: Engine | None = field(default=None, init=False, repr=False)

    @property
    def uow_factory(self) -> UowFactory:
        if self._uow_factory is None:
            db_url = self.config.get_ruta_bdd()
            factory, engine = build_uow_factory(db_url=db_url)
            self._uow_factory = factory
            self._engine = engine
        return self._uow_factory

    def ensure_database_schema(self) -> tuple[bool, str]:
        """Aplica migraciones Alembic pendientes para garantizar compatibilidad de esquema."""
        db_url = self.config.get_ruta_bdd()
        if not db_url:
            return False, "No hay URL de base de datos configurada."
        return run_alembic_upgrade(db_url)

    def reload_database(self, new_db_url: str | None = None) -> None:
        """Reinicia la conexión tras cambiar la URL de BDD en configuración."""
        if new_db_url is not None:
            self.config.set_new_bbd_route_in_config(new_db_url)
        if self._engine is not None:
            self._engine.dispose()
        self._engine = None
        self._uow_factory = None
        reset_uow_factory()

    def close(self) -> None:
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
        self._uow_factory = None
