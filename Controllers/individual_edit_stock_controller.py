from Views.individual_edit_stock_popup import VentanaEditIndividual
from Services.ProductoService import ProductoService

class IndividualEditStockController:
    def __init__(self, invoqued_by_window, products_ids):
        self.view = VentanaEditIndividual(invoqued_by_window, self)
        self.producto_service = ProductoService()
        self.products_ids = products_ids

        self.view.render_view()


    def get_products_to_edit(self):
        productos = self.producto_service.get_products_by_id_list(self.products_ids)
        self.view.pasar_al_cuadro(productos)


    def confirmar_cambios(self, quantity: int):

        if quantity < 0:
            self.view.show_error('Error con la cantidad de stock, La cantidad a agregar solo puede '
                                                                      'ser un numero entero positivo')

        self.producto_service.add_stock_to_multiple_products(self.products_ids, quantity)

        self.view.cambios_realizados()

