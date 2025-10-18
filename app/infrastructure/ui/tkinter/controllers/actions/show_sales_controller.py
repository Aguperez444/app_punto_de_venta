from datetime import datetime

from app.application.use_cases.query_sales import QuerySales
from app.infrastructure.database.sqlalchemy.uow_factory import uow_factory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.models.venta import Venta
    from app.infrastructure.ui.tkinter.views.views.show_sales_list_view import ShowSalesListView

class ShowSalesController:
    def __init__(self, view: 'ShowSalesListView'):
        self.view = view
        self.uow_factory = uow_factory


    def finished_init(self):
        self.view.render_view()

    def get_ventas_del_dia(self, fecha: datetime):


        listado_ventas = QuerySales(self.uow_factory).by_date(fecha)

        self.view.pasar_al_cuadro_ventas(listado_ventas)

        total_ventas = self.calculate_total_of_sales(listado_ventas)
        self.view.mostrar_total_ventas(f'{total_ventas}')


    def get_ventas_del_mes(self, fecha: datetime):

        listado_ventas = QuerySales(self.uow_factory).by_month(fecha.year, fecha.month)

        self.view.pasar_al_cuadro_ventas(listado_ventas)

        total_ventas = self.calculate_total_of_sales(listado_ventas)
        self.view.mostrar_total_ventas(f'{total_ventas}')


    @staticmethod
    def calculate_total_of_sales(ventas: list['Venta']) -> float:
        if len(ventas) == 0:
            return 0.00
        total = sum(venta.total_price for venta in ventas)
        return total #TODO usar DTO's para las ventas, evitar llevar objetos price hasta acá