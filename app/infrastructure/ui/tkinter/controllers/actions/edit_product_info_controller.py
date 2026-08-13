from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.application.use_cases.delete_product import DeleteProduct, RestoreProduct
from app.application.use_cases.query_products import QueryProducts
from app.domain.custom_errors import DomainValidationError
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_info_controller import (
    IndividualEditInfoController,
)

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.edit_product_info_view import EditProductInfoView

logger = logging.getLogger(__name__)


class EditProductInfoController:
    def __init__(self, view: "EditProductInfoView", uow_factory_param=None):
        self.view = view
        container = getattr(view, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )

    def finished_init(self):
        self.view.render_view()

    def get_all_products(self, include_inactive: bool = False):
        productos = QueryProducts(self.uow_factory).get_all(include_inactive=include_inactive)
        self.view.pasar_al_cuadro(productos)

    def get_all_products_alphabetically(self, include_inactive: bool = False):
        productos = QueryProducts(self.uow_factory).get_all_alphabetically(
            include_inactive=include_inactive
        )
        self.view.pasar_al_cuadro(productos)

    def get_filtered_products(self, search_criteria: str, include_inactive: bool = False):
        found_products = QueryProducts(self.uow_factory).get_filtered(
            search_criteria, include_inactive=include_inactive
        )
        if found_products:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def get_filtered_products_alphabetically(
        self, search_criteria: str, include_inactive: bool = False
    ):
        found_products = QueryProducts(self.uow_factory).get_filtered_alphabetically(
            search_criteria, include_inactive=include_inactive
        )
        if found_products:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def open_individual_edit_info_window(self, id_producto: int):
        IndividualEditInfoController(self.view, id_producto, uow_factory_param=self.uow_factory)

    def delete_product(self, id_producto: int) -> bool:
        try:
            DeleteProduct(self.uow_factory).execute(id_producto)
            self.view.show_message("Producto eliminado (archivado) correctamente.")
            return True
        except DomainValidationError as dve:
            logger.warning("No se pudo eliminar producto %s: %s", id_producto, dve)
            self.view.show_error(str(dve))
            return False
        except Exception as exc:
            logger.exception("Error inesperado al eliminar producto %s", id_producto)
            self.view.show_error(f"Error al eliminar el producto: {exc}")
            return False

    def restore_product(self, id_producto: int) -> bool:
        try:
            RestoreProduct(self.uow_factory).execute(id_producto)
            self.view.show_message("Producto reactivado correctamente.")
            return True
        except DomainValidationError as dve:
            logger.warning("No se pudo reactivar producto %s: %s", id_producto, dve)
            self.view.show_error(str(dve))
            return False
        except Exception as exc:
            logger.exception("Error inesperado al reactivar producto %s", id_producto)
            self.view.show_error(f"Error al reactivar el producto: {exc}")
            return False
