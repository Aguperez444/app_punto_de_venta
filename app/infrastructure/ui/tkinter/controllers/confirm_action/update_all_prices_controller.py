from app.infrastructure.ui.tkinter.views.popups.update_all_prices_popup import UpdateAllPricesPopup

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.edit_prices_view import EditPricesView

class UpdateAllPricesController:
    def __init__(self, invoked_by_window: 'EditPricesView'):
        self.view = UpdateAllPricesPopup(invoked_by_window, self)
        self.main_window = invoked_by_window

        self.view.render_view()


    def confirmar_cambios(self):
        self.view.destroy()
        self.main_window.confirmar_cambios()

    def cancelar_cambios(self):
        self.view.destroy()
        self.main_window.realizar_busqueda() # Refrescar la vista principal sin cambios