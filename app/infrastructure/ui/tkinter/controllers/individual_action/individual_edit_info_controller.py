import logging

from app.application.use_cases.query_products import QueryProducts
from app.domain.custom_errors import DomainValidationError
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.ui.tkinter.views.popups.individual_edit_info_popup import IndividualEditInfoPopup
from app.application.use_cases.edit_product_info import EditProductInfo

logger = logging.getLogger(__name__)


class IndividualEditInfoController:
    def __init__(self, invoked_by_window, mod_id: int):
        self.main_window = invoked_by_window
        self.mod_id = mod_id
        self.uow_factory = uow_factory
        self.view = IndividualEditInfoPopup(invoked_by_window, self)

        self.view.render_view()


    def get_product_info(self) -> None:
        producto = QueryProducts(self.uow_factory).get_by_id(self.mod_id)

        if producto is None:
            self.view.show_error("No se encontró el producto seleccionado.")
            self.view.destroy()
            return

        self.view.pasar_al_cuadro([producto])
        self.view.mostrar_datos(producto)

    def update_product(self, new_data: dict) -> None:
        try:
            EditProductInfo(self.uow_factory).execute(self.mod_id, new_data['nombre'],
                                                           new_data['codigo'], new_data['precio'],
                                                           new_data['stock'], new_data['detalle'],
                                                           new_data['codigo_de_barras'])

            self.view.show_message("Producto actualizado correctamente.")
            self.view.destroy()
            self.main_window.realizar_busqueda()
        except (ValueError, DomainValidationError) as e:
            logger.warning("Error de validación al editar producto %s: %s", self.mod_id, e)
            self.view.show_error(str(e))
        except Exception as e:
            logger.exception("Error inesperado al actualizar producto %s", self.mod_id)
            self.view.show_error(f"Error al actualizar el producto: {e}")

    def cancelar_cambios(self):
        self.view.destroy()
        self.main_window.realizar_busqueda()
