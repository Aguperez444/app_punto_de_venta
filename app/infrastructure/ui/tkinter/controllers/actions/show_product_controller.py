from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.application.services.sale_cart import SaleCart
from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.register_sale import RegisterSale
from app.domain.custom_errors import DomainValidationError
from app.domain.models.producto import Producto
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.ui.tkinter.controllers.individual_action.register_sale_controller import (
    RegisterSaleController,
)
from app.infrastructure.ui.tkinter.views.popups.cart_checkout_popup import CartCheckoutPopup

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.show_products_view import ShowProductsView

logger = logging.getLogger(__name__)


class ShowProductController:
    def __init__(self, view: "ShowProductsView", uow_factory_param=None):
        self.view = view
        self.venta_controller = None
        container = getattr(view, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )
        self.clock = container.clock if container is not None else None
        self.cart = SaleCart()

    def search_products(self, search_criteria: str):
        found_products = QueryProducts(self.uow_factory).get_filtered(search_criteria)
        if found_products:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def search_products_alphabetically(self, search_criteria: str):
        found_products = QueryProducts(self.uow_factory).get_filtered_alphabetically(search_criteria)
        if found_products:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def open_sale_register_window(self, product_id: str | int):
        try:
            product_id_int = int(product_id)
        except ValueError:
            self.view.show_error(
                "El id del producto es incorrecto, informe al administrador del sistema"
            )
            return

        self.venta_controller = RegisterSaleController(
            self,
            self.view,
            product_id_int,
            uow_factory_param=self.uow_factory,
            cart=self.cart,
        )

    def try_open_by_exact_barcode(self, code: str) -> bool:
        cleaned = (code or "").strip()
        if not cleaned:
            return False
        product = QueryProducts(self.uow_factory).get_by_barcode(cleaned)
        if product is not None and product.id_producto is not None:
            self.open_sale_register_window(product.id_producto)
            return True
        return False

    def add_product_to_cart(self, product: Producto, quantity: int) -> None:
        self.cart.add_item(product, quantity)
        self.notify_cart_changed()

    def notify_cart_changed(self) -> None:
        if hasattr(self.view, "update_cart_summary"):
            self.view.update_cart_summary(
                items_count=self.cart.items_count,
                total_units=self.cart.total_units,
                total_str=str(self.cart.total),
            )

    def clear_cart(self) -> None:
        self.cart.clear()
        self.notify_cart_changed()

    def open_cart_checkout(self) -> None:
        if self.cart.is_empty:
            self.view.show_message("El carrito está vacío.")
            return
        CartCheckoutPopup(self.view, self, self.cart)

    def confirm_cart_sale(self, parent_popup=None) -> bool:
        if self.cart.is_empty:
            return False
        target = parent_popup or self.view
        try:
            sale_id = RegisterSale(self.uow_factory, clock=self.clock).execute_cart(
                self.cart.to_sale_items()
            )
        except DomainValidationError as dve:
            logger.warning("Validación fallida al confirmar carrito: %s", dve)
            target.show_error(str(dve))
            return False
        except Exception as exc:
            logger.exception("Error inesperado al confirmar venta del carrito")
            target.show_error(f"Error al registrar la venta del carrito: {exc}")
            return False

        self.cart.clear()
        self.notify_cart_changed()
        target.show_message(f"Venta #{sale_id} registrada correctamente.")
        self.view.realizar_busqueda()
        return True

    def finished_init(self):
        self.view.render_view()
        self.notify_cart_changed()
