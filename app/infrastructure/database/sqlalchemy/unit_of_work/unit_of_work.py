from typing import Callable, Protocol
from sqlalchemy.orm import Session

from app.application.ports.producto_repository import IProductoRepository
from app.application.ports.sale_repository import ISaleRepository

SessionFactory = Callable[[], Session]

class IUnitOfWork(Protocol):

    product_repo: IProductoRepository | None
    sale_repo: ISaleRepository | None
    session: Session | None

    def __enter__(self) -> 'IUnitOfWork':
        pass

    def __exit__(self, exc_type, exc, tb) -> None:
        pass


    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

UowFactory = Callable[[], IUnitOfWork]