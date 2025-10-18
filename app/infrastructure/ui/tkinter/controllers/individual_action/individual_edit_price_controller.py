from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.update_price import UpdatePrice
from app.infrastructure.ui.tkinter.views.popups.individual_edit_price_popup import IndividualEditPricePopup
from app.infrastructure.database.sqlalchemy.uow_factory import uow_factory

class IndividualEditPriceController:

    def __init__(self, invoked_by_window, mod_ids_in: list[int]):
        self.view = IndividualEditPricePopup(invoked_by_window, self)
        self.main_window = invoked_by_window
        self.uow_factory = uow_factory
        self.mod_ids_in = mod_ids_in

        self.view.render_view()

    def get_products(self):

        productos = QueryProducts(self.uow_factory).get_by_id_list(self.mod_ids_in)

        self.view.pasar_al_cuadro(productos)

    def update_price_by_percentage(self, porcentaje_str: str):
        try:
            porcentaje = float(porcentaje_str)
        except ValueError:
            self.view.show_error("Porcentaje debe ser un numero válido")
            return

        try:

            UpdatePrice(self.uow_factory).update_selected(self.mod_ids_in, porcentaje)
        except Exception as e:
            self.view.show_error(str(e))
            raise e #TODO ENVIAR ERRORES A UN LOGGER
        self.view.show_message("Se han actualizado correctamente los precios")
        self.view.destroy()
        self.main_window.realizar_busqueda()

    def update_price_to_new(self, nuevo_precio_str):
        try:

            UpdatePrice(self.uow_factory).update_to_new_value(self.mod_ids_in, nuevo_precio_str)
        except ValueError:
            self.view.show_error("El precio debe ser un número válido")
        except Exception as e:
            self.view.show_error(str(e))
            raise e #TODO ENVIAR ERRORES A UN LOGGER

        self.view.show_message("Se han actualizado correctamente los precios")
        self.view.destroy()
        self.main_window.realizar_busqueda()


    def cancelar_cambios(self):
        self.view.destroy()
        self.main_window.realizar_busqueda()
