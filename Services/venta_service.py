from datetime import datetime, timedelta
from Models.venta import Venta
from Repositories.venta_repository import VentaRepository


class VentaService:
    def __init__(self):
        self.repo = VentaRepository()

    @staticmethod
    def create_sale(time: datetime) -> Venta:

        new_sale = Venta(fecha=time, total_price=0)

        return new_sale

    def save_sale(self, nueva_venta: Venta) -> bool:
        try:
            self.repo.save_venta(nueva_venta)
        except Exception:
            return False
        return True

    def update_total_price(self, venta: Venta, new_total_price: float) -> bool:
        try:
            self.repo.update_venta_total_price(venta, new_total_price)
        except Exception:
            return False
        return True

    def find_sale_by_date(self, date: datetime) -> list[Venta]:
        inicio = datetime(date.year, date.month, date.day, 0, 0, 0)
        fin = inicio + timedelta(days=1)
        ventas = self.repo.find_ventas_by_date(inicio, fin)
        return ventas

    def find_sales_in_date_range(self, start_date: datetime, end_date: datetime) -> list[Venta]:
        ventas = self.repo.find_ventas_by_date(start_date, end_date)
        return ventas

    def find_sales_in_month(self, year: int, month: int) -> list[Venta]:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        ventas = self.repo.find_ventas_by_date(start_date, end_date)
        return ventas

    def update_sale(self, venta: Venta) -> bool:
        try:
            self.repo.update_venta(venta)
        except Exception:
            return False
        return True
