from abc import ABC, abstractmethod
from app.domain.models.producto import Producto
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock


class IProductoRepository(ABC):
    updated: list

    @abstractmethod
    def save_product(self, product: Producto) -> None:
        pass

    @abstractmethod
    def get_all_products(self) -> list[Producto]:
        pass
    @abstractmethod
    def get_all_products_alphabetically(self) -> list[Producto]:
        pass

    @abstractmethod
    def get_filtered(self, buscado: str) -> list[Producto] | None:
        pass

    @abstractmethod
    def get_filtered_alphabetically(self, search_criteria: str) -> list[Producto] | None:
        pass

    @abstractmethod
    def get_all_no_stock(self) -> list[Producto] | None:
        pass

    @abstractmethod
    def get_all_no_stock_alphabetically(self) -> list[Producto] | None:
        pass

    @abstractmethod
    def get_filtered_no_stock(self, buscado: str) -> list[Producto] | None:
        pass

    @abstractmethod
    def get_filtered_no_stock_alphabetically(self, buscado: str) -> list[Producto] | None:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Producto | None:
        pass

    @abstractmethod
    def get_products_by_id_list(self, ids_buscadas: list[int]) -> list[Producto] | None:
        pass

    @abstractmethod
    def add_stock(self, id_producto: int, cantidad: int) -> None:
        pass

    @abstractmethod
    def add_stock_to_multiple_products(self, ids_list: list, stock_to_add: int) -> None:
        pass

    @abstractmethod
    def set_stock(self, id_producto: int, cantidad: Stock) -> None:
        pass

    @abstractmethod
    def update_all_prices(self, percent_multiplier: float = 1) -> None:
        pass

    @abstractmethod
    def update_selected_product_prices(self, ids_list: list, percent_multiplier: float = 1) -> None:
        pass

    @abstractmethod
    def update_price_to_new_value(self, ids_list: list, new_price: Precio) -> None:
        pass

    @abstractmethod
    def set_stock_bulk(self, ids_list: list, new_stock: Stock) -> None:
        pass

    @abstractmethod
    def update_info_product(self, producto_new: Producto) -> None:
        pass





