from __future__ import annotations

from app.application.ports.unit_of_work import UowFactory
from app.domain.custom_errors import NotFoundProductError


class DeleteProduct:
    """Desactiva (baja lógica) un producto preservando la integridad de ventas históricas."""

    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def execute(self, product_id: int) -> None:
        with self.uow_factory() as uow:
            found = uow.product_repo.set_active(product_id, False)
            if not found:
                raise NotFoundProductError(f"No existe el producto con ID {product_id}.")
            uow.commit()


class RestoreProduct:
    """Reactiva un producto previamente dado de baja lógica."""

    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def execute(self, product_id: int) -> None:
        with self.uow_factory() as uow:
            found = uow.product_repo.set_active(product_id, True)
            if not found:
                raise NotFoundProductError(f"No existe el producto con ID {product_id}.")
            uow.commit()
