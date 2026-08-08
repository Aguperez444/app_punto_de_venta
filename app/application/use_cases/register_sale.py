from __future__ import annotations

from datetime import datetime

from app.application.ports.clock import IClock
from app.application.ports.unit_of_work import UowFactory
from app.domain.custom_errors import NotFoundProductError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import Venta


class RegisterSale:
    def __init__(self, uow_factory: UowFactory, clock: IClock | None = None):
        self.uow_factory = uow_factory
        self.clock = clock

    def execute(self, product_id: int, amount: int, date: datetime | None = None) -> int:
        sale_date = date or (self.clock.now() if self.clock is not None else datetime.now())
        with self.uow_factory() as uow:
            product = uow.product_repo.get_by_id(product_id)

            if not product:
                raise NotFoundProductError("Producto inexistente")
            product.disminuir_stock(amount)

            venta = Venta.nueva(sale_date)
            venta.agregar_detalle(DetalleVenta.create_new(product_id, amount, product.precio))
            venta.validar_no_vacia()

            uow.sale_repo.save_new(venta)
            uow.product_repo.set_stock(product.id_producto, product.stock)
            uow.commit()
        return venta.id_venta
