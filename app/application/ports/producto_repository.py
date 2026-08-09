from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from app.domain.models.precio import Precio
from app.domain.models.producto import Producto
from app.domain.models.stock import Stock


@dataclass(frozen=True)
class ProductFilter:
    """Criterios unificados de búsqueda, orden y paginación para productos."""

    search: str | None = None
    only_no_stock: bool = False
    alphabetical: bool = False
    include_inactive: bool = False
    limit: int | None = None
    offset: int = 0


class IProductoRepository(ABC):
    @abstractmethod
    def save_product(self, product: Producto) -> None:
        pass

    @abstractmethod
    def list_products(self, filtro: ProductFilter | None = None) -> list[Producto]:
        pass

    @abstractmethod
    def count_products(self, filtro: ProductFilter | None = None) -> int:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Producto | None:
        pass

    @abstractmethod
    def get_by_barcode(self, barcode: str) -> Producto | None:
        pass

    @abstractmethod
    def get_products_by_id_list(self, ids_buscadas: list[int]) -> list[Producto]:
        pass

    @abstractmethod
    def add_stock(self, id_producto: int, cantidad: int) -> None:
        pass

    @abstractmethod
    def add_stock_to_multiple_products(self, ids_list: list[int], stock_to_add: int) -> None:
        pass

    @abstractmethod
    def set_stock(self, id_producto: int, cantidad: Stock) -> None:
        pass

    @abstractmethod
    def set_stock_bulk(self, ids_list: list[int], new_stock: Stock) -> None:
        pass

    @abstractmethod
    def update_all_prices(self, percent_multiplier: Decimal = Decimal("1")) -> None:
        pass

    @abstractmethod
    def update_selected_product_prices(
        self, ids_list: list[int], percent_multiplier: Decimal = Decimal("1")
    ) -> None:
        pass

    @abstractmethod
    def update_price_to_new_value(self, ids_list: list[int], new_price: Precio) -> None:
        pass

    @abstractmethod
    def update_info_product(self, producto_new: Producto) -> None:
        pass

    @abstractmethod
    def set_active(self, product_id: int, active: bool) -> bool:
        pass

    # Conveniencias de compatibilidad delegando a list_products
    def get_all_products(self) -> list[Producto]:
        return self.list_products(ProductFilter())

    def get_all_products_alphabetically(self) -> list[Producto]:
        return self.list_products(ProductFilter(alphabetical=True))

    def get_filtered(self, buscado: str) -> list[Producto]:
        if not buscado or not buscado.strip():
            return []
        return self.list_products(ProductFilter(search=buscado))

    def get_filtered_alphabetically(self, search_criteria: str) -> list[Producto]:
        if not search_criteria or not search_criteria.strip():
            return []
        return self.list_products(ProductFilter(search=search_criteria, alphabetical=True))

    def get_all_no_stock(self) -> list[Producto]:
        return self.list_products(ProductFilter(only_no_stock=True))

    def get_all_no_stock_alphabetically(self) -> list[Producto]:
        return self.list_products(ProductFilter(only_no_stock=True, alphabetical=True))

    def get_filtered_no_stock(self, buscado: str) -> list[Producto]:
        if not buscado or not buscado.strip():
            return []
        return self.list_products(ProductFilter(search=buscado, only_no_stock=True))

    def get_filtered_no_stock_alphabetically(self, buscado: str) -> list[Producto]:
        if not buscado or not buscado.strip():
            return []
        return self.list_products(
            ProductFilter(search=buscado, only_no_stock=True, alphabetical=True)
        )
