from __future__ import annotations

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.sqlalchemy.engine_factory import create_db_engine
from app.infrastructure.database.sqlalchemy.unit_of_work.unit_of_work_impl import (
    SqlAlchemyUnitOfWork,
)

_engine: Engine | None = None
_session_factory: sessionmaker | None = None


def reset_uow_factory() -> None:
    """Limpia el engine y session_factory en caché (útil al cambiar la BDD o en tests)."""
    global _engine, _session_factory
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_factory = None


def build_uow_factory(db_url: str | None = None):
    """Construye una fábrica de UoW explícita para una URL dada."""
    engine = create_db_engine(db_url=db_url)
    session_local = sessionmaker(bind=engine)

    def _factory() -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(session_local)

    return _factory, engine


def _ensure_initialized() -> sessionmaker:
    global _engine, _session_factory
    if _session_factory is None:
        _engine = create_db_engine()
        _session_factory = sessionmaker(bind=_engine)
    return _session_factory


def uow_factory() -> SqlAlchemyUnitOfWork:
    """Crea una nueva SqlAlchemyUnitOfWork inicializando el engine de forma perezosa."""
    return SqlAlchemyUnitOfWork(_ensure_initialized())
