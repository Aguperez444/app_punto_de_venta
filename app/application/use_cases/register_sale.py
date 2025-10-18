from datetime import datetime
from app.domain.custom_errors import NotFoundProductError
from app.domain.models.venta import Venta
from app.domain.models.detalle_venta import DetalleVenta
from app.infrastructure.database.sqlalchemy.unit_of_work_impl import UowFactory


class RegisterSale:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def execute(self, product_id: int, amount: int, date: datetime | None = None) -> int:
            with self.uow_factory() as uow:
                product = uow.product_repo.get_by_id(product_id)

                if not product:
                    raise NotFoundProductError("Producto inexistente")
                product.disminuir_stock(amount)

                venta = Venta.nueva(date)
                venta.agregar_detalle(DetalleVenta.create_new(product_id, amount, product.precio))
                venta.update_price()


                uow.sale_repo.save_new(venta)     # repo persiste venta + detalles y copia total
                uow.product_repo.update_info_product(product) # TODO podría cambiarse el update info por un update_stock
                uow.commit()
            return venta.id_venta