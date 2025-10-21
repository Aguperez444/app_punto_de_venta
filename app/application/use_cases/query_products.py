from app.domain.models.producto import Producto
from app.infrastructure.database.sqlalchemy.unit_of_work.unit_of_work_impl import UowFactory



class QueryProducts:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory


    # region general
    def get_all(self) -> list[Producto]:
        with self.uow_factory() as uow:
            return uow.product_repo.get_all_products()


    def get_all_alphabetically(self) -> list[Producto]:
        with self.uow_factory() as uow:
            return uow.product_repo.get_all_products_alphabetically()


    def get_filtered(self, buscado: str) -> list[Producto] | None:
        with self.uow_factory() as uow:
            return uow.product_repo.get_filtered(buscado)


    def get_filtered_alphabetically(self, search_criteria: str) -> list[Producto] | None:
        with self.uow_factory() as uow:
            return uow.product_repo.get_filtered_alphabetically(search_criteria)

    # endregion

    # region no_stock
    def get_no_stock(self) -> list[Producto]:
        with self.uow_factory() as uow:
         return uow.product_repo.get_all_no_stock()


    def get_no_stock_alphabetically(self) -> list[Producto] | None:
        with self.uow_factory() as uow:
         return uow.product_repo.get_all_no_stock_alphabetically()


    def get_filtered_no_stock(self, buscado: str) -> list[Producto] | None:
        with self.uow_factory() as uow:
            return uow.product_repo.get_filtered_no_stock(buscado)


    def get_filtered_no_stock_alphabetically(self, buscado: str) -> list[Producto] | None:
        with self.uow_factory() as uow:
            return uow.product_repo.get_filtered_no_stock_alphabetically(buscado)
    # endregion

    # region by id
    def get_by_id(self, product_id: int) -> Producto | None:
        with self.uow_factory() as uow:
            return uow.product_repo.get_by_id(product_id)

    def get_by_id_list(self, ids_buscadas: list[int]) -> list[Producto] | None:
        with self.uow_factory() as uow:
            return uow.product_repo.get_products_by_id_list(ids_buscadas)
    # endregion


    def get_product_name_by_id(self, product_id: int) -> str:
        with self.uow_factory() as uow:
            producto = uow.product_repo.get_by_id(product_id)
            if producto:
                return producto.nombre
        return ''