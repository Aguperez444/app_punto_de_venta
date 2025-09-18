from Controllers.individual_edit_stock_controller import IndividualEditStockController
from Views.add_stock_window import AddStockWindow
from Services.producto_service import ProductoService

class AddStockController:
    def __init__(self, invoqued_by_window):
        self.view = AddStockWindow(invoqued_by_window, self)
        self.producto_service = ProductoService()

        self.view.render_view()


    def get_all_products(self):
        products = self.producto_service.get_all_products()
        self.view.pasar_al_cuadro(products)


    def get_all_products_alphabetically(self):
        products = self.producto_service.get_all_products_alphabetically()
        self.view.pasar_al_cuadro(products)


    def get_filtered_products(self, search_term):
        products = self.producto_service.get_products_by_str_filter(search_term)
        self.view.pasar_al_cuadro(products)

    def open_individual_edit_window(self, mod_ids):
        IndividualEditStockController(self.view, mod_ids)  # abre la ventana de edición individual

