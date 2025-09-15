from Views.add_stock_window import VentanaStock
from Services.ProductoService import ProductoService

class AddStockController:
    def __init__(self, invoqued_by_window):
        self.view = VentanaStock(invoqued_by_window, self)
        self.producto_service = ProductoService()

        self.view.render_view()


    def get_all_products(self):
        products = self.producto_service.get_all_products()
        self.view.pasar_al_cuadro(products)


    def get_all_products_alphabetically(self):
        products = self.producto_service.get_all_products_alphabetically()
        self.view.pasar_al_cuadro(products)


    def search_products(self, search_term):
        products = self.producto_service.get_products_by_str_filter(search_term)
        self.view.pasar_al_cuadro(products)