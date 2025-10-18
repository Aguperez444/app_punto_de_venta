from app.application.use_cases.query_products import QueryProducts
from app.infrastructure.database.sqlalchemy.uow_factory import uow_factory

from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_info_controller import IndividualEditInfoController

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.edit_product_info_view import EditProductInfoView


class EditProductInfoController:
    def __init__(self, view: 'EditProductInfoView'):
        self.view = view
        self.uow_factory = uow_factory

    def finished_init(self):
        self.view.render_view()


    def get_all_products(self):
        productos = QueryProducts(self.uow_factory).get_all()
        self.view.pasar_al_cuadro(productos)

    def get_all_products_alphabetically(self):

        productos = QueryProducts(self.uow_factory).get_all_alphabetically()
        self.view.pasar_al_cuadro(productos)

    def get_filtered_products(self, search_criteria: str):

        found_products = QueryProducts(self.uow_factory).get_filtered(search_criteria)
        if found_products is not None:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()


    def get_filtered_products_alphabetically(self, search_criteria: str):
        found_products = QueryProducts(self.uow_factory).get_filtered_alphabetically(search_criteria)
        if found_products is not None:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def open_individual_edit_info_window(self, id_producto):
        IndividualEditInfoController(self.view, id_producto)

