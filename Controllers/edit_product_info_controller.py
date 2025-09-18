from Controllers.individual_edit_info_controller import IndividualEditInfoController
from Views.edit_product_info_window import EditProductInfoWindow
from Services.producto_service import ProductoService

class EditProductInfoController:
    def __init__(self, invoqued_by_window):
        self.product_service = ProductoService()
        self.view = EditProductInfoWindow(invoqued_by_window, self)

        self.view.render_view()


    def get_all_products(self):
        productos = self.product_service.get_all_products()
        self.view.pasar_al_cuadro(productos)


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

    def open_individual_edit_info_window(self, id_producto):
        IndividualEditInfoController(self.view, id_producto)