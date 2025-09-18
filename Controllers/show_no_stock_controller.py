from Controllers.individual_edit_stock_controller import IndividualEditStockController
from Views.show_no_stock_list_window import VentanaNoStock
from Services.producto_service import ProductoService

class ShowNoStockController:
    def __init__(self, invoqued_by_window):

        self.product_service = ProductoService()
        self.view = VentanaNoStock(invoqued_by_window, self)

        self.view.render_view()

    def get_all_products_no_stock(self):
        productos = self.product_service.get_all_products_no_stock()
        self.view.pasar_al_cuadro(productos)

    def get_filtered_products_no_stock(self, filtro_busqueda):
        productos = self.product_service.get_products_by_str_filter_no_stock(filtro_busqueda)
        self.view.pasar_al_cuadro(productos)

    def get_filtered_products_no_stock_alphabetically(self, filtro_busqueda):
        productos = self.product_service.get_products_by_str_filter_no_stock_alphabetically(filtro_busqueda)
        self.view.pasar_al_cuadro(productos)

    def open_edit_stock_controller_window(self, mod_ids):
        IndividualEditStockController(self.view, mod_ids)  # abre la ventana de edición individual