from typing import Callable
from sqlalchemy.orm import Session


from app.infrastructure.database.sqlalchemy.unit_of_work.unit_of_work import IUnitOfWork
from app.infrastructure.database.sqlalchemy.repositories.producto_repository_impl import ProductoRepositoryImpl
from app.infrastructure.database.sqlalchemy.repositories.venta_repository_impl import SaleRepositoryImpl


SessionFactory = Callable[[], Session]

class SqlAlchemyUnitOfWork(IUnitOfWork):
    """
        UoW mínimo: crea una Session al entrar, hace commit/rollback al salir.
        Acepta un session_factory (por ej. `SessionLocal = session_maker(...)`).
        """

    def __init__(self, session_factory: SessionFactory) -> None:
        self._sf = session_factory
        # propiedades inicializadas en __enter__
        self.session: Session
        self.product_repo: ProductoRepositoryImpl
        self.sale_repo: SaleRepositoryImpl

    # Context manager
    def __enter__(self) -> 'SqlAlchemyUnitOfWork':
        self.session: Session = self._sf()  # nueva Session por acción
        self.product_repo: ProductoRepositoryImpl = ProductoRepositoryImpl(self.session)
        self.sale_repo: SaleRepositoryImpl = SaleRepositoryImpl(self.session)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
            self.session = None
            self.product_repo = None
            self.sale_repo = None


    def commit(self) -> None:
        assert self.session is not None, "UoW sin session (¿usaste 'with uow:'?)"
        self.session.commit()

    def rollback(self) -> None:
        assert self.session is not None, "UoW sin session"
        self.session.rollback()

UowFactory = Callable[[], IUnitOfWork]