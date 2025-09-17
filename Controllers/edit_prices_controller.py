from Views.edit_prices_window import VentanaPrecios
from Services.ProductoService import ProductoService

class EditPricesController:
    def __init__(self, invoqued_by_window):
        self.product_service = ProductoService()

        self.view = VentanaPrecios(invoqued_by_window, self)
        self.view.render_view()


    def get_all_products(self):
        productos = self.product_service.get_all_products()
        self.view.pasar_al_cuadro(productos)

    def update_all_prices(self, percentage_str: str):
        try:
            percentage = float(percentage_str)
        except ValueError:
            self.view.show_error('Error con el porcentaje, El porcentaje debe ser un numero valido')
            return

        self.product_service.update_all_prices(percentage)
        self.view.cambios_realizados()

    def get_filtered_products(self, search_criteria: str):
        found_products = self.product_service.get_products_by_str_filter(search_criteria)
        if found_products is not None:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()

    def get_filtered_products_alphabetically(self, search_criteria: str):
        found_products = self.product_service.get_products_by_str_filter_alphabetically(search_criteria)
        if found_products is not None:
            self.view.pasar_al_cuadro(found_products)
        else:
            self.view.clean_treeview()