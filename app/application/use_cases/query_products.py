from __future__ import annotations

from app.application.ports.producto_repository import ProductFilter
from app.application.ports.unit_of_work import UowFactory
from app.domain.models.producto import Producto


class QueryProducts:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def list_products(self, filtro: ProductFilter | None = None) -> list[Producto]:
        with self.uow_factory() as uow:
            return uow.product_repo.list_products(filtro)

    def count_products(self, filtro: ProductFilter | None = None) -> int:
        with self.uow_factory() as uow:
            return uow.product_repo.count_products(filtro)

    # region general
    def get_all(self, include_inactive: bool = False, limit: int | None = None) -> list[Producto]:
        with self.uow_factory() as uow:
            if include_inactive or limit is not None:
                return uow.product_repo.list_products(
                    ProductFilter(include_inactive=include_inactive, limit=limit)
                )
            return uow.product_repo.get_all_products()

    def get_all_alphabetically(
        self, include_inactive: bool = False, limit: int | None = None
    ) -> list[Producto]:
        with self.uow_factory() as uow:
            if include_inactive or limit is not None:
                return uow.product_repo.list_products(
                    ProductFilter(
                        alphabetical=True, include_inactive=include_inactive, limit=limit
                    )
                )
            return uow.product_repo.get_all_products_alphabetically()

    def get_filtered(
        self, buscado: str, include_inactive: bool = False, limit: int | None = None
    ) -> list[Producto]:
        if not buscado or not buscado.strip():
            return []
        with self.uow_factory() as uow:
            if include_inactive or limit is not None:
                return uow.product_repo.list_products(
                    ProductFilter(
                        search=buscado, include_inactive=include_inactive, limit=limit
                    )
                )
            return uow.product_repo.get_filtered(buscado) or []

    def get_filtered_alphabetically(
        self, search_criteria: str, include_inactive: bool = False, limit: int | None = None
    ) -> list[Producto]:
        if not search_criteria or not search_criteria.strip():
            return []
        with self.uow_factory() as uow:
            if include_inactive or limit is not None:
                return uow.product_repo.list_products(
                    ProductFilter(
                        search=search_criteria,
                        alphabetical=True,
                        include_inactive=include_inactive,
                        limit=limit,
                    )
                )
            return uow.product_repo.get_filtered_alphabetically(search_criteria) or []

    # endregion

    # region no_stock
    def get_no_stock(self) -> list[Producto]:
        with self.uow_factory() as uow:
            return uow.product_repo.get_all_no_stock() or []

    def get_no_stock_alphabetically(self) -> list[Producto]:
        with self.uow_factory() as uow:
            return uow.product_repo.get_all_no_stock_alphabetically() or []

    def get_filtered_no_stock(self, buscado: str) -> list[Producto]:
        if not buscado or not buscado.strip():
            return []
        with self.uow_factory() as uow:
            return uow.product_repo.get_filtered_no_stock(buscado) or []

    def get_filtered_no_stock_alphabetically(self, buscado: str) -> list[Producto]:
        if not buscado or not buscado.strip():
            return []
        with self.uow_factory() as uow:
            return uow.product_repo.get_filtered_no_stock_alphabetically(buscado) or []

    # endregion

    # region by id / barcode
    def get_by_id(self, product_id: int) -> Producto | None:
        with self.uow_factory() as uow:
            return uow.product_repo.get_by_id(product_id)

    def get_by_barcode(self, barcode: str) -> Producto | None:
        with self.uow_factory() as uow:
            return uow.product_repo.get_by_barcode(barcode)

    def get_by_id_list(self, ids_buscadas: list[int]) -> list[Producto]:
        with self.uow_factory() as uow:
            return uow.product_repo.get_products_by_id_list(ids_buscadas) or []

    # endregion

    def get_product_name_by_id(self, product_id: int) -> str:
        with self.uow_factory() as uow:
            producto = uow.product_repo.get_by_id(product_id)
            if producto:
                return producto.nombre
        return ""
