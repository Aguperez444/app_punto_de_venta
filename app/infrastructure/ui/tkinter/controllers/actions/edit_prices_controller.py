from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_price_controller import IndividualEditPriceController
from app.infrastructure.ui.tkinter.controllers.confirm_action.update_all_prices_controller import UpdateAllPricesController
from app.application.use_cases.update_price import UpdatePrice
from app.application.use_cases.query_products import QueryProducts
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.edit_prices_view import EditPricesView

class EditPricesController:
    def __init__(self, view: 'EditPricesView'):
        self.uow_factory = uow_factory
        self.view = view


    def finished_init(self):
        self.view.render_view()


    def get_all_products(self):

        productos = QueryProducts(self.uow_factory).get_all()

        if productos is not None:
            self.view.pasar_al_cuadro(productos)
        else:
            self.view.clean_treeview()

    def update_all_prices(self, percentage_str: str):
        try:
            percentage = float(percentage_str)
        except ValueError:
            self.view.show_error('Error con el porcentaje, El porcentaje debe ser un numero valido')
            return

        UpdatePrice(self.uow_factory).update_all(percentage)
        self.view.cambios_realizados(percentage)

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

    def get_all_products_alphabetically(self):
        productos = QueryProducts(self.uow_factory).get_all_alphabetically()
        print("entro alpha")

        self.view.pasar_al_cuadro(productos)

    def open_individual_edit_price_window(self, mod_ids):
        IndividualEditPriceController(self.view, mod_ids)

    def open_update_all_prices_window(self):
        UpdateAllPricesController(self.view)

