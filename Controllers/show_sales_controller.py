from datetime import datetime
from Views.show_sales_list_window import ShowSalesListWindow
from Services.venta_service import VentaService


class ShowSalesController:
    def __init__(self, invoqued_by_window):
        self.view_pointer = ShowSalesListWindow(invoqued_by_window, self)
        self.sales_service_pointer = VentaService()

        self.view_pointer.render_view()

    def get_ventas_del_dia(self, fecha: datetime):
        listado_ventas = self.sales_service_pointer.find_sale_by_date(fecha)
        self.view_pointer.pasar_al_cuadro_ventas(listado_ventas)

        total_ventas = self.calculate_total_of_sales(listado_ventas)
        self.view_pointer.mostrar_total_ventas(f'${total_ventas}')


    def get_ventas_del_mes(self, fecha: datetime):
        listado_ventas = self.sales_service_pointer.find_sales_in_month(fecha.year, fecha.month)

        print('\n'*4 + '-'*60 + '\n')
        print(listado_ventas)
        for venta in listado_ventas:
            print(venta)
            print(venta.detalles)
            for detalle in venta.detalles:
                print(f'   {detalle}')
                print(f'        {detalle.producto}')
        print('\n'*4 + '-'*60 + '\n')

        self.view_pointer.pasar_al_cuadro_ventas(listado_ventas)

        total_ventas = self.calculate_total_of_sales(listado_ventas)
        self.view_pointer.mostrar_total_ventas(f'${total_ventas}')


    @staticmethod
    def calculate_total_of_sales(ventas):
        if len(ventas) == 0:
            return 0.00
        total = sum(venta.total_price for venta in ventas)
        return round(total, 2)