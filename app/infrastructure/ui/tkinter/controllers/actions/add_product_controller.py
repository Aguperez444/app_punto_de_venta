from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.application.use_cases.add_product import AddProduct
from app.domain.custom_errors import DomainValidationError
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.add_product_view import AddProductsView

logger = logging.getLogger(__name__)


class AddProductController:
    _REQUIRED_FIELDS = ("nombre", "codigo", "precio", "stock")

    def __init__(self, view: "AddProductsView", uow_factory_param=None):
        container = getattr(view, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )
        self.view = view

    def finished_init(self):
        self.view.render_view()

    def add_product(self, product_data: dict) -> bool:
        missing = [
            field
            for field in self._REQUIRED_FIELDS
            if not str(product_data.get(field, "")).strip()
        ]
        if missing:
            self.view.show_error(
                f"Completá los campos obligatorios: {', '.join(missing)}"
            )
            return False

        try:
            AddProduct(self.uow_factory).execute(
                nombre=str(product_data["nombre"]).strip(),
                codigo=str(product_data["codigo"]).strip(),
                precio_param=str(product_data["precio"]).strip(),
                detalle=str(product_data.get("detalle", "")).strip(),
                codigo_de_barras=str(product_data.get("codigo_de_barras", "")).strip(),
                stock_param=str(product_data["stock"]).strip(),
            )
            self.view.show_success_message()
            if hasattr(self.view, "product_entry_fields"):
                self.view.product_entry_fields.reset_input_fields()
            return True
        except DomainValidationError as dve:
            logger.warning("Validación fallida al agregar producto: %s", dve)
            self.view.show_error_message(str(dve))
            return False
        except Exception as e:
            logger.exception("Error inesperado al agregar producto")
            self.view.show_error_message(f"Error al agregar el producto: {e}")
            return False
