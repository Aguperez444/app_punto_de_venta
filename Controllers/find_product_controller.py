from Services.ProductoService import ProductoService
from Views.search_window import VentanaBuscar
from Controllers.register_sale_controller import RegisterSaleController

class FindProductController:
    def __init__(self, invoqued_by_window):
        self.view_pointer = VentanaBuscar(invoqued_by_window, self)
        self.product_service = ProductoService()
        self.venta_controller = None


    def search_products(self, search_criteria: str):
        found_products = self.product_service.get_products_by_str_filter(search_criteria)
        if found_products is not None:
            self.view_pointer.pasar_al_cuadro(found_products)
        else:
            self.view_pointer.clean_treeview()


    def open_sale_register_window(self, product_id: int):
        self.venta_controller = RegisterSaleController(self, self.view_pointer, product_id)