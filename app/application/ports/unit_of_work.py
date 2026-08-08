from __future__ import annotations

from typing import Callable, Protocol

from app.application.ports.producto_repository import IProductoRepository
from app.application.ports.sale_repository import ISaleRepository


class IUnitOfWork(Protocol):
    """Puerto de Unidad de Trabajo independiente de la tecnología de persistencia."""

    product_repo: IProductoRepository
    sale_repo: ISaleRepository

    def __enter__(self) -> "IUnitOfWork":
        ...

    def __exit__(self, exc_type, exc, tb) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


UowFactory = Callable[[], IUnitOfWork]
