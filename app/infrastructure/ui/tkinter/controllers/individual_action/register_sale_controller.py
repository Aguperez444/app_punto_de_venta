from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.register_sale import RegisterSale
from app.domain.custom_errors import DomainValidationError
from app.domain.models.detalle_venta import DetalleVenta
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.ui.tkinter.views.popups.sale_register_popup import SalesRegisterWindow

if TYPE_CHECKING:
    from app.application.services.sale_cart import SaleCart

logger = logging.getLogger(__name__)


class RegisterSaleController:
    def __init__(
        self,
        invoked_by_controller,
        invoked_by_window,
        product_id: int,
        uow_factory_param=None,
        cart: "SaleCart | None" = None,
    ):
        self.parent_controller = invoked_by_controller
        self.product_id = product_id
        self.main_window = invoked_by_window
        self.cart = cart
        container = getattr(invoked_by_window, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )
        self.clock = container.clock if container is not None else None

        default_to_cart = bool(self.cart is not None and self.cart.has_items)
        self.view = SalesRegisterWindow(
            invoked_by_window, self, default_to_cart=default_to_cart
        )
        self.view.render_view()

    def show_product_data(self):
        product = self.get_product_data()
        if product is None:
            self.view.show_error("No se encontró el producto seleccionado.")
            self.view.destroy()
            return
        self.view.adjust_product_text(product.nombre, current_stock=product.stock.value)
        self.view.pasar_al_cuadro([product])

    def get_product_data(self):
        return QueryProducts(self.uow_factory).get_by_id(self.product_id)

    def _parse_quantity(self, quantity_sold: str) -> int | None:
        try:
            qty = int(str(quantity_sold).strip())
            if qty <= 0:
                raise DomainValidationError("La cantidad vendida debe ser un número positivo.")
            return qty
        except DomainValidationError as dve:
            self.view.show_error(str(dve))
            return None
        except ValueError:
            self.view.show_error(
                "La cantidad vendida debe ser un número entero válido, no se aceptan letras o símbolos."
            )
            return None

    def add_to_cart(self, quantity_sold: str) -> None:
        qty = self._parse_quantity(quantity_sold)
        if qty is None:
            return
        product_data = self.get_product_data()
        if product_data is None:
            self.view.show_error("No se encontró el producto seleccionado.")
            return

        if hasattr(self.parent_controller, "add_product_to_cart"):
            self.parent_controller.add_product_to_cart(product_data, qty)
        elif self.cart is not None:
            self.cart.add_item(product_data, qty)

        self.view.destroy()
        if hasattr(self.main_window, "focus_search_after_cart_add"):
            self.main_window.focus_search_after_cart_add()

    def register_new_sale(self, quantity_sold: str) -> None:
        qty = self._parse_quantity(quantity_sold)
        if qty is None:
            return

        product_data = self.get_product_data()
        if product_data is None:
            self.view.show_error("No se encontró el producto seleccionado.")
            return

        try:
            date = self.get_fecha_hora_actual()
            sale_id = RegisterSale(self.uow_factory, clock=self.clock).execute(
                product_data.id_producto, qty, date
            )
            success = bool(sale_id)
        except DomainValidationError as dve:
            logger.warning("Validación fallida al registrar venta: %s", dve)
            self.view.show_error(str(dve))
            return
        except Exception as e:
            logger.exception("Error inesperado al registrar la venta del producto %s", self.product_id)
            self.view.show_error(
                f"Error desconocido al registrar la venta. Por favor, "
                f"contacte al administrador del sistema: {e}"
            )
            return

        if success:
            self.view.show_message("Venta registrada correctamente.")
            self.main_window.realizar_busqueda()
            self.view.destroy()
        else:
            self.view.show_error("Error al registrar la venta. Por favor, inténtelo de nuevo.")

    def get_fecha_hora_actual(self) -> datetime:
        return self.clock.now() if self.clock is not None else datetime.now()

    @staticmethod
    def calculate_total_price(detalles_list: list[DetalleVenta]):
        return sum(detalle.calcular_subtotal() for detalle in detalles_list)
