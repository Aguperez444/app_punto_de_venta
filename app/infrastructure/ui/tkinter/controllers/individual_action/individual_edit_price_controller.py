import logging

from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.update_price import UpdatePrice
from app.domain.custom_errors import PriceInvalidError
from app.infrastructure.ui.tkinter.views.popups.individual_edit_price_popup import IndividualEditPricePopup
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory

logger = logging.getLogger(__name__)

class IndividualEditPriceController:

    def __init__(self, invoked_by_window, mod_ids_in: list[int], uow_factory_param=None):
        self.view = IndividualEditPricePopup(invoked_by_window, self)
        self.main_window = invoked_by_window
        container = getattr(invoked_by_window, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )
        self.mod_ids_in = mod_ids_in

        self.view.render_view()

    def get_products(self):

        productos = QueryProducts(self.uow_factory).get_by_id_list(self.mod_ids_in)

        self.view.pasar_al_cuadro(productos)

    def update_price_by_percentage(self, porcentaje_str: str):
        try:
            UpdatePrice(self.uow_factory).update_selected(self.mod_ids_in, porcentaje_str)
        except ValueError as e:
            logger.warning("Porcentaje inválido en edición individual: %s", e)
            self.view.show_error(str(e))
            return
        except Exception as e:
            logger.exception("Error al actualizar precios por porcentaje")
            self.view.show_error(str(e))
            return
        self.view.show_message("Se han actualizado correctamente los precios")
        self.view.destroy()
        self.main_window.realizar_busqueda()

    def update_price_to_new(self, nuevo_precio_str):
        try:
            UpdatePrice(self.uow_factory).update_to_new_value(self.mod_ids_in, nuevo_precio_str)
        except (ValueError, PriceInvalidError) as e:
            logger.warning("Precio inválido ingresado: %s", e)
            self.view.show_error(f"El precio debe ser un número válido: {e}")
            return
        except Exception as e:
            logger.exception("Error inesperado al actualizar precio manual")
            self.view.show_error(str(e))
            return

        self.view.show_message("Se han actualizado correctamente los precios")
        self.view.destroy()
        self.main_window.realizar_busqueda()


    def cancelar_cambios(self):
        self.view.destroy()
        self.main_window.realizar_busqueda()
