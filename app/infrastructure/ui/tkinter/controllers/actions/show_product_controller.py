from app.application.use_cases.query_products import QueryProducts
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.ui.tkinter.controllers.individual_action.register_sale_controller import RegisterSaleController

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.show_products_view import ShowProductsView


class ShowProductController:
    def __init__(self, view: 'ShowProductsView'):
        self.view = view
        self.venta_controller = None
        self.uow_factory = uow_factory

    def search_products(self, search_criteria: str):

        found_products = QueryProducts(self.uow_factory).get_filtered(search_criteria)

        if found_products is not None:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def open_sale_register_window(self, product_id: str):

        try:
            product_id_int = int(product_id)
        except ValueError:
            self.view.show_error("El id del producto es incorrecto, informe al administrador del sistema")
            return

        self.venta_controller = RegisterSaleController(self, self.view, product_id_int)

    def finished_init(self):
        self.view.render_view()

