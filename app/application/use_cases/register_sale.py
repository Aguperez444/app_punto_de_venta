from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.application.ports.clock import IClock
from app.application.ports.unit_of_work import UowFactory
from app.domain.custom_errors import EmptySaleError, NotFoundProductError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.producto import Producto
from app.domain.models.venta import Venta


@dataclass(frozen=True)
class SaleItemInput:
    """Ítem de entrada para registrar una venta con uno o más productos."""

    product_id: int
    amount: int


class RegisterSale:
    def __init__(self, uow_factory: UowFactory, clock: IClock | None = None):
        self.uow_factory = uow_factory
        self.clock = clock

    def execute(self, product_id: int, amount: int, date: datetime | None = None) -> int:
        """Venta rápida de un único producto."""
        return self.execute_cart([SaleItemInput(product_id=product_id, amount=amount)], date=date)

    def execute_cart(self, items: list[SaleItemInput], date: datetime | None = None) -> int:
        """
        Registra una venta atómica con uno o múltiples productos.
        Agrupa cantidades repetidas de un mismo product_id y permite stock negativo por regla de negocio.
        """
        if not items:
            raise EmptySaleError("No se puede registrar una venta sin productos.")

        aggregated: dict[int, int] = {}
        for item in items:
            if item.amount <= 0:
                raise ValueError("La cantidad vendida debe ser mayor a 0.")
            aggregated[item.product_id] = aggregated.get(item.product_id, 0) + item.amount

        sale_date = date or (self.clock.now() if self.clock is not None else datetime.now())

        with self.uow_factory() as uow:
            products_by_id: dict[int, Producto] = {}
            for product_id in aggregated:
                product = uow.product_repo.get_by_id(product_id)
                if not product:
                    raise NotFoundProductError(f"Producto inexistente (ID {product_id})")
                products_by_id[product_id] = product

            venta = Venta.nueva(sale_date)
            for product_id, amount in aggregated.items():
                product = products_by_id[product_id]
                product.disminuir_stock(amount)
                venta.agregar_detalle(DetalleVenta.create_new(product_id, amount, product.precio))

            venta.validar_no_vacia()
            uow.sale_repo.save_new(venta)

            for product in products_by_id.values():
                uow.product_repo.set_stock(product.id_producto, product.stock)

            uow.commit()

        return venta.id_venta
