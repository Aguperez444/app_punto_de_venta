from __future__ import annotations

import logging

from app.application.use_cases.edit_stock import EditStock
from app.application.use_cases.query_products import QueryProducts
from app.domain.custom_errors import DomainValidationError
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.ui.tkinter.views.popups.individual_edit_stock_popup import (
    IndividualEditStockPopup,
)

logger = logging.getLogger(__name__)


class IndividualEditStockController:
    def __init__(self, invoked_by_window, products_ids: list[int], uow_factory_param=None):
        container = getattr(invoked_by_window, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )
        self.products_ids = list(products_ids)
        self.view = IndividualEditStockPopup(invoked_by_window, self)
        self.view.render_view()

    def get_products_to_edit(self) -> None:
        products = QueryProducts(self.uow_factory).get_by_id_list(self.products_ids)
        self.view.pasar_al_cuadro(products)

    def confirmar_cambios(self, quantity_raw: int | str, mode: str = "add") -> None:
        try:
            quantity = int(str(quantity_raw).strip())
        except ValueError:
            self.view.show_error("Ingrese un número entero válido para la cantidad de stock.")
            return

        use_case = EditStock(self.uow_factory)
        try:
            if mode == "add":
                if quantity <= 0:
                    self.view.show_error("La cantidad a sumar debe ser un entero positivo.")
                    return
                use_case.add_stock_to_multiple_products(self.products_ids, quantity)
            elif mode == "subtract":
                if quantity <= 0:
                    self.view.show_error("La cantidad a restar debe ser un entero positivo.")
                    return
                # Regla de negocio: el stock resultante puede quedar negativo
                use_case.add_stock_to_multiple_products(self.products_ids, -quantity)
            elif mode == "set":
                use_case.set_stock_bulk(self.products_ids, quantity)
            else:
                self.view.show_error(f"Modo de ajuste de stock desconocido: {mode}")
                return
        except (ValueError, DomainValidationError) as exc:
            logger.warning("Error de validación al actualizar stock: %s", exc)
            self.view.show_error(str(exc))
            return
        except Exception as exc:
            logger.exception("Error inesperado al actualizar stock")
            self.view.show_error(f"Error al actualizar stock: {exc}")
            return

        self.view.cambios_realizados()
