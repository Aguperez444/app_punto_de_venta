from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.edit_stock import EditStock
from app.infrastructure.ui.tkinter.views.popups.individual_edit_stock_popup import IndividualEditStockPopup
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory


class IndividualEditStockController:
    def __init__(self, invoked_by_window, products_ids):
        self.view = IndividualEditStockPopup(invoked_by_window, self)
        self.uow_factory = uow_factory
        self.products_ids = products_ids

        self.view.render_view()


    def get_products_to_edit(self):

        products = QueryProducts(self.uow_factory).get_by_id_list(self.products_ids)

        self.view.pasar_al_cuadro(products)


    def confirmar_cambios(self, quantity: int):

        if quantity < 0:
            self.view.show_error('Error con la cantidad de stock, La cantidad a agregar solo puede '
                                                                      'ser un numero entero positivo')


        EditStock(self.uow_factory).add_stock_to_multiple_products(self.products_ids, quantity)

        self.view.cambios_realizados()

    #TODO IMPLEMENTAR FORMA PARA DISMINUIR EL STOCK