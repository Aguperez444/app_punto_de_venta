from app.domain.models.producto import Producto
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock

from app.infrastructure.database.sqlalchemy.unit_of_work.unit_of_work_impl import UowFactory


class EditProductInfo:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory


    def execute(self, id_producto: int, nombre: str, codigo: str, precio: str,
                stock_param: str, detalle: str, codigo_de_barras: str):

        price = Precio.from_string(precio)
        stock = Stock.from_string(stock_param)

        product = Producto(id_producto=id_producto, nombre=nombre, codigo=codigo, precio=price,
                           detalle=detalle, codigo_de_barras=codigo_de_barras, stock=stock)

        with self.uow_factory() as uow:
            uow.product_repo.update_info_product(product)
            uow.commit()

        return

