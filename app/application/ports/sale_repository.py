from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.models.venta import Venta


class ISaleRepository(ABC):
    @abstractmethod
    def find_ventas_by_date(self, initial_date: datetime, final_date: datetime) -> list[Venta]:
        pass

    @abstractmethod
    def get_by_id(self, venta_id: int) -> Venta | None:
        pass

    @abstractmethod
    def save_new(self, venta: Venta) -> None:
        pass
