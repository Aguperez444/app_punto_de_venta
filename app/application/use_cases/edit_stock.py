from app.domain.models.stock import Stock
from app.infrastructure.database.sqlalchemy.unit_of_work_impl import UowFactory


class EditStock:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def add_stock(self, id_producto: int, cantidad: int) -> None:
        with self.uow_factory() as uow:
            uow.product_repo.add_stock(id_producto, cantidad)
            uow.commit()
        return


    def add_stock_to_multiple_products(self, ids_list: list[int], stock_to_add: int) -> None:
        if not ids_list:
            return
        with self.uow_factory as uow:
            for id_producto in ids_list:
                uow.product_repo.add_stock(id_producto, stock_to_add)
            uow.commit()
        return


    def set_stock(self, id_producto: int, cantidad: int) -> None:
        stock = Stock(cantidad)
        with self.uow_factory() as uow:
            uow.product_repo.set_stock(id_producto, stock)
            uow.commit()


    def set_stock_bulk(self, ids_list: list[int], new_stock: int):
        if not ids_list:
            return
        stock = Stock(new_stock)
        with self.uow_factory() as uow:
            uow.product_repo.set_stock_bulk(ids_list, stock)
            uow.commit()