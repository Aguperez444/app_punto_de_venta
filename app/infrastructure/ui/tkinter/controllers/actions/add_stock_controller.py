from app.application.use_cases.query_products import QueryProducts
from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_stock_controller import IndividualEditStockController
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.add_stock_view import AddStockView


class AddStockController:
    def __init__(self, view: 'AddStockView', uow_factory_param=None):
        self.view = view
        container = getattr(view, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )


    def finished_init(self):
        self.view.render_view()


    def get_all_products(self):
        products = QueryProducts(self.uow_factory).get_all()

        self.view.pasar_al_cuadro(products)


    def get_all_products_alphabetically(self):
        products = QueryProducts(self.uow_factory).get_all_alphabetically()

        self.view.pasar_al_cuadro(products)


    def get_filtered_products(self, search_term: str):
        products = QueryProducts(self.uow_factory).get_filtered(search_term)
        if products is not None:
            self.view.pasar_al_cuadro(products)
        else:
            self.view.clean_treeview()


    def get_filtered_products_alphabetically(self, search_criteria: str):
        found_products = QueryProducts(self.uow_factory).get_filtered_alphabetically(search_criteria)

        if found_products is not None:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()


    def open_individual_edit_window(self, mod_ids: list[int]):
        IndividualEditStockController(self.view, mod_ids)  # abre la ventana de edición individual_action