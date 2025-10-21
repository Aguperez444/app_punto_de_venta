
from app.domain.models.producto import Producto


from app.infrastructure.database.sqlalchemy.unit_of_work.unit_of_work_impl import UowFactory


class AddProduct:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def execute(self, nombre: str, codigo: str, precio_param: str,
                detalle: str, codigo_de_barras: str, stock_param: str) -> Producto:

        with self.uow_factory() as uow:
            nuevo_producto = Producto.from_string(nombre, codigo, precio_param, detalle, codigo_de_barras, stock_param)

            uow.product_repo.save_product(nuevo_producto)
            uow.commit()
            return nuevo_producto

