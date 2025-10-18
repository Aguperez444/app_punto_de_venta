from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from app.domain.models.precio import Precio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.domain.models.detalle_venta import DetalleVenta


class Venta:
    def __init__(self, id_venta: int | None, total_price: Precio, fecha: datetime, detalles: list['DetalleVenta']):
        self._id_venta = id_venta
        self._total_price = total_price
        self._fecha = fecha
        self._detalles = detalles

    @property
    def id_venta(self) -> int:
        return self._id_venta

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def total(self) -> Decimal:
        return Decimal(sum(detalle.calcular_subtotal() for detalle in self._detalles)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    @classmethod
    def nueva(cls, date: datetime | None = None) -> "Venta":
        return cls(id_venta=None, fecha=date or datetime.now(), total_price=Precio(Decimal("0")), detalles=[])


    def agregar_detalle(self, detalle: 'DetalleVenta') -> None:
        self._detalles.append(detalle)


    def update_price(self):
        self._total_price = Precio(self.total)

    @property
    def total_price(self):
        return self._total_price

    @property
    def detalles(self):
        return self._detalles

    @id_venta.setter
    def id_venta(self, value):
        self._id_venta = value