from Services.ProductoService import ProductoService
from Views.update_all_prices_popup import VentanaIndividualEditPrice

class UpdateAllPricesController:
    def __init__(self, invoqued_by_window):
        self.view = VentanaIndividualEditPrice(invoqued_by_window, self)
        self.main_window = invoqued_by_window
        self.producto_service = ProductoService()

        self.view.render_view()


    def confirmar_cambios(self):
        self.main_window.confirmar_cambios()
        self.view.destroy()

    def cancelar_cambios(self):
        self.view.destroy()
        self.main_window.realizar_busqueda() # Refrescar la vista principal sin cambios