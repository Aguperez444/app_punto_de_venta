from Views.individual_edit_info_popup import IndividualEditInfoPopup
from Services.producto_service import ProductoService


class IndividualEditInfoController:
    def __init__(self, invoqued_by_window, mod_ids_in: int):
        self.product_service = ProductoService()
        self.main_window = invoqued_by_window
        self.mod_ids_in = mod_ids_in
        self.view = IndividualEditInfoPopup(invoqued_by_window, self)

        self.view.render_view()


    def get_product_info(self) -> None:
        producto = self.product_service.get_product_by_id(self.mod_ids_in)


        self.view.pasar_al_cuadro([producto]) # TODO CHECK THIS, unificar forma de pasar al cuadro
        self.view.adjust_geometry() # Ajustar la geometría de la ventana para que el cuadro sea visible
        self.view.mostrar_datos(producto)

    def update_product(self, new_data: dict) -> None:
        try:
            self.product_service.update_product_info(self.mod_ids_in, new_data)
            self.view.show_message("Producto actualizado correctamente.")
            self.view.destroy()
            self.main_window.realizar_busqueda()
        except ValueError as e:
            self.view.show_error(str(e))
            return

    def cancelar_cambios(self):
        self.view.destroy()
        self.main_window.realizar_busqueda()
