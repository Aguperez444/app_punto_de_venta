from __future__ import annotations

import logging
from typing import Callable

from sqlalchemy.orm import Session

from app.application.ports.unit_of_work import IUnitOfWork, UowFactory
from app.infrastructure.database.sqlalchemy.repositories.producto_repository_impl import (
    ProductoRepositoryImpl,
)
from app.infrastructure.database.sqlalchemy.repositories.venta_repository_impl import (
    SaleRepositoryImpl,
)

logger = logging.getLogger(__name__)
SessionFactory = Callable[[], Session]


class SqlAlchemyUnitOfWork(IUnitOfWork):
    """
    Unidad de Trabajo sobre SQLAlchemy.
    Política explícita: el caso de uso de escritura debe llamar a `commit()`.
    Si ocurre una excepción o se sale del contexto sin commit, hace rollback y cierra la sesión.
    """

    def __init__(self, session_factory: SessionFactory) -> None:
        self._sf = session_factory
        self.session: Session | None = None
        self.product_repo: ProductoRepositoryImpl | None = None  # type: ignore[assignment]
        self.sale_repo: SaleRepositoryImpl | None = None  # type: ignore[assignment]
        self._committed = False

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._sf()
        self.product_repo = ProductoRepositoryImpl(self.session)
        self.sale_repo = SaleRepositoryImpl(self.session)
        self._committed = False
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if self.session is not None:
                if exc_type is not None or not self._committed:
                    self.session.rollback()
                    if exc_type is not None:
                        logger.debug("UoW rollback por excepción: %s", exc)
        finally:
            if self.session is not None:
                self.session.close()
            self.session = None
            self.product_repo = None  # type: ignore[assignment]
            self.sale_repo = None  # type: ignore[assignment]
            self._committed = False

    def commit(self) -> None:
        assert self.session is not None, "UoW sin session (¿usaste 'with uow:'?)"
        self.session.commit()
        self._committed = True

    def rollback(self) -> None:
        assert self.session is not None, "UoW sin session"
        self.session.rollback()
        self._committed = False


__all__ = ["SqlAlchemyUnitOfWork", "SessionFactory", "UowFactory"]
