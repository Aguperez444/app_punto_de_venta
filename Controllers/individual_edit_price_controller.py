from Views.individual_edit_price_popup import IndividualEditPricePopup
from Services.producto_service import ProductoService


class IndividualEditPriceController:

    def __init__(self, invoqued_by_window, mod_ids_in: list[int]):
        self.view = IndividualEditPricePopup(invoqued_by_window, self)
        self.main_window = invoqued_by_window
        self.producto_service = ProductoService() #TODO CHECK THIS
        self.mod_ids_in = mod_ids_in

        self.view.render_view()

    def get_products(self):
        productos = self.producto_service.get_products_by_id_list(self.mod_ids_in)

        self.view.pasar_al_cuadro(productos)

    def update_price_by_percentage(self, porcentaje_str: str):
        try:
            porcentaje = float(porcentaje_str)
        except ValueError:
            self.view.show_error("Porcentaje debe ser un numero válido")
            return

        self.producto_service.update_selected_product_prices(self.mod_ids_in, porcentaje)
        self.view.show_message("Se han actualizado correctamente los precios")
        self.view.destroy()
        self.main_window.realizar_busqueda()

    def update_price_to_new(self, nuevo_precio_str):
        try:
            self.producto_service.update_price_to_new_value(self.mod_ids_in, nuevo_precio_str)
        except ValueError:
            self.view.show_error("Porcentaje debe ser un número válido")
            return

        self.view.show_message("Se han actualizado correctamente los precios")
        self.view.destroy()
        self.main_window.realizar_busqueda()


    def cancelar_cambios(self):
        self.view.destroy()
        self.main_window.realizar_busqueda()