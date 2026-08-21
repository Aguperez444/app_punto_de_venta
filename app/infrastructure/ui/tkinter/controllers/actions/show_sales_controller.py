from __future__ import annotations

import logging
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from app.application.dto.sales_dto import SaleDetailDTO, SaleSummaryDTO
from app.application.use_cases.query_sales import QuerySales
from app.domain.models.precio import Precio
from app.domain.models.venta import Venta
from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.infrastructure.export.csv_exporter import CsvExporter
from app.infrastructure.ui.tkinter.views.popups.sale_detail_popup import SaleDetailPopup

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.show_sales_list_view import ShowSalesListView

logger = logging.getLogger(__name__)


class ShowSalesController:
    def __init__(self, view: "ShowSalesListView", uow_factory_param=None):
        self.view = view
        container = getattr(view, "container", None)
        self.uow_factory = (
            uow_factory_param
            or (container.uow_factory if container is not None else uow_factory)
        )
        self._last_sales: list[Venta] = []

    @property
    def last_sales(self) -> list[Venta]:
        return list(self._last_sales)

    def finished_init(self):
        self.view.render_view()

    def get_ventas_del_dia(self, fecha: datetime):
        listado_ventas = QuerySales(self.uow_factory).by_date(fecha)
        self._present_sales(listado_ventas)

    def get_ventas_del_mes(self, fecha: datetime):
        listado_ventas = QuerySales(self.uow_factory).by_month(fecha.year, fecha.month)
        self._present_sales(listado_ventas)

    def _present_sales(self, ventas: list[Venta]) -> None:
        self._last_sales = list(ventas)
        summaries = [SaleSummaryDTO.from_domain(v) for v in ventas]
        self.view.pasar_al_cuadro_ventas(summaries)
        total_ventas = self.calculate_total_of_sales(ventas)
        self.view.mostrar_total_ventas(str(total_ventas))

    def open_sale_detail(self, venta_id: int) -> None:
        try:
            venta = QuerySales(self.uow_factory).get_by_id(venta_id)
        except Exception as exc:
            logger.exception("Error al obtener detalle de venta %s", venta_id)
            self.view.show_error(f"No se pudo cargar el detalle de la venta: {exc}")
            return

        if venta is None:
            self.view.show_error("No se encontró la venta seleccionada.")
            return

        detail_dto = SaleDetailDTO.from_domain(venta)
        SaleDetailPopup(self.view, detail_dto)

    def export_current_sales_to_csv(self, output_path: str) -> bool:
        if not self._last_sales:
            self.view.show_error("No hay ventas listadas para exportar.")
            return False
        try:
            CsvExporter.export_sales(self._last_sales, output_path)
            self.view.show_message(f"Ventas exportadas correctamente a:\n{output_path}")
            return True
        except Exception as exc:
            logger.exception("Error al exportar ventas a CSV")
            self.view.show_error(f"Error al exportar ventas: {exc}")
            return False

    @staticmethod
    def calculate_total_of_sales(ventas: list[Venta]) -> Precio:
        if not ventas:
            return Precio(Decimal("0.00"))
        total = sum((venta.total_price.value for venta in ventas), Decimal("0.00"))
        return Precio(total)
