from app.application.use_cases.query_products import QueryProducts
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_stock_controller import IndividualEditStockController

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.show_no_stock_list_view import ShowNoStockView

class ShowNoStockController:
    def __init__(self, view: 'ShowNoStockView'):

        self.uow_factory = uow_factory
        self.view = view

    def finished_init(self):
        self.view.render_view()

    def get_all_products_no_stock(self):
        productos = QueryProducts(self.uow_factory).get_no_stock()
        self.mostrar(productos)

    def get_all_products_no_stock_alphabetically(self):
        productos = QueryProducts(self.uow_factory).get_no_stock_alphabetically()
        self.mostrar(productos)

    def get_filtered_products_no_stock(self, filtro_busqueda):
        productos = QueryProducts(self.uow_factory).get_filtered_no_stock(filtro_busqueda)
        self.mostrar(productos)

    def get_filtered_products_no_stock_alphabetically(self, filtro_busqueda):
        productos = QueryProducts(self.uow_factory).get_filtered_no_stock_alphabetically(filtro_busqueda)
        self.mostrar(productos)


    def mostrar(self, productos):
        if productos is not None:
            self.view.pasar_al_cuadro(productos)
        else:
            self.view.clean_treeview()

    def open_edit_stock_controller_window(self, mod_ids):
        IndividualEditStockController(self.view, mod_ids)  # abre la ventana de edición individual_action



