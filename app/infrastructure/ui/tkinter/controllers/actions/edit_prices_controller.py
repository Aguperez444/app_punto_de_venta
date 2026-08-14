from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.update_price import UpdatePrice
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.ui.tkinter.controllers.confirm_action.update_all_prices_controller import (
    UpdateAllPricesController,
)
from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_price_controller import (
    IndividualEditPriceController,
)

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.edit_prices_view import EditPricesView

logger = logging.getLogger(__name__)


class EditPricesController:
    def __init__(self, view: "EditPricesView", uow_factory_param=None):
        container = getattr(view, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )
        self.view = view

    def finished_init(self):
        self.view.render_view()

    def get_all_products(self):
        productos = QueryProducts(self.uow_factory).get_all()
        if productos:
            self.view.pasar_al_cuadro(productos)
        else:
            self.view.clean_treeview()

    def update_all_prices(self, percentage_str: str):
        try:
            UpdatePrice(self.uow_factory).update_all(percentage_str)
        except ValueError as exc:
            logger.warning("Porcentaje inválido al actualizar todos los precios: %s", exc)
            self.view.show_error(str(exc))
            return
        except Exception as exc:
            logger.exception("Error inesperado al actualizar todos los precios")
            self.view.show_error(f"Error al actualizar los precios: {exc}")
            return

        self.view.cambios_realizados(percentage_str)

    def get_filtered_products(self, search_criteria: str):
        found_products = QueryProducts(self.uow_factory).get_filtered(search_criteria)
        if found_products:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def get_filtered_products_alphabetically(self, search_criteria: str):
        found_products = QueryProducts(self.uow_factory).get_filtered_alphabetically(search_criteria)
        if found_products:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def get_all_products_alphabetically(self):
        productos = QueryProducts(self.uow_factory).get_all_alphabetically()
        self.view.pasar_al_cuadro(productos)

    def open_individual_edit_price_window(self, mod_ids: list[int]):
        if not mod_ids:
            return
        IndividualEditPriceController(self.view, mod_ids, uow_factory_param=self.uow_factory)

    def open_update_all_prices_window(self):
        UpdateAllPricesController(self.view)
