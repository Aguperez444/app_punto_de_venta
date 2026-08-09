from __future__ import annotations

from datetime import datetime, timedelta

from app.application.ports.unit_of_work import UowFactory
from app.domain.models.venta import Venta


class QuerySales:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def get_by_id(self, venta_id: int) -> Venta | None:
        with self.uow_factory() as uow:
            return uow.sale_repo.get_by_id(venta_id)

    def by_date(self, date: datetime) -> list[Venta]:
        inicio = datetime(date.year, date.month, date.day, 0, 0, 0)
        fin = inicio + timedelta(days=1)
        with self.uow_factory() as uow:
            ventas = uow.sale_repo.find_ventas_by_date(inicio, fin)
        return ventas

    def by_range(self, start_date: datetime, end_date: datetime) -> list[Venta]:
        with self.uow_factory() as uow:
            ventas = uow.sale_repo.find_ventas_by_date(start_date, end_date)
        return ventas

    def by_month(self, year: int, month: int) -> list[Venta]:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        with self.uow_factory() as uow:
            ventas = uow.sale_repo.find_ventas_by_date(start_date, end_date)
        return ventas
