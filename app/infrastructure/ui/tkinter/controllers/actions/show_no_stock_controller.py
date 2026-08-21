import logging

from app.application.use_cases.query_products import QueryProducts
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.export.csv_exporter import CsvExporter
from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_stock_controller import IndividualEditStockController

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.show_no_stock_list_view import ShowNoStockView

logger = logging.getLogger(__name__)


class ShowNoStockController:
    def __init__(self, view: 'ShowNoStockView', uow_factory_param=None):
        container = getattr(view, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )
        self.view = view
        self._last_products = []

    def finished_init(self):
        self.view.render_view()

    def get_all_products_no_stock(self):
        productos = QueryProducts(self.uow_factory).get_no_stock()
        self.mostrar(productos)

    def get_all_products_no_stock_alphabetically(self):
        productos = QueryProducts(self.uow_factory).get_no_stock_alphabetically()
        self.mostrar(productos)

    def get_filtered_products_no_stock(self, filtro_busqueda):
        productos = QueryProducts(self.uow_factory).get_filtered_no_stock(filtro_busqueda)
        self.mostrar(productos)

    def get_filtered_products_no_stock_alphabetically(self, filtro_busqueda):
        productos = QueryProducts(self.uow_factory).get_filtered_no_stock_alphabetically(filtro_busqueda)
        self.mostrar(productos)


    def mostrar(self, productos):
        self._last_products = list(productos) if productos else []
        if self._last_products:
            self.view.pasar_al_cuadro(self._last_products)
        else:
            self.view.clean_treeview()

    def export_no_stock_to_csv(self, output_path: str) -> bool:
        if not self._last_products:
            self.view.show_error("No hay productos sin stock para exportar.")
            return False
        try:
            CsvExporter.export_products(self._last_products, output_path)
            self.view.show_message(f"Lista de faltantes exportada correctamente a:\n{output_path}")
            return True
        except Exception as exc:
            logger.exception("Error al exportar productos sin stock a CSV")
            self.view.show_error(f"Error al exportar lista de faltantes: {exc}")
            return False

    def open_edit_stock_controller_window(self, mod_ids):
        if not mod_ids:
            return
        IndividualEditStockController(self.view, mod_ids, uow_factory_param=self.uow_factory)



