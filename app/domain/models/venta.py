from __future__ import annotations

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import TYPE_CHECKING

from app.domain.custom_errors import EmptySaleError
from app.domain.models.precio import Precio

if TYPE_CHECKING:
    from app.domain.models.detalle_venta import DetalleVenta


class Venta:
    def __init__(
        self,
        id_venta: int | None,
        total_price: Precio,
        fecha: datetime,
        detalles: list["DetalleVenta"],
    ):
        self._id_venta = id_venta
        self._total_price = total_price
        self._fecha = fecha
        self._detalles = list(detalles)

    @property
    def id_venta(self) -> int | None:
        return self._id_venta

    @id_venta.setter
    def id_venta(self, value: int | None) -> None:
        self._id_venta = value

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def total(self) -> Decimal:
        subtotal = sum((detalle.calcular_subtotal() for detalle in self._detalles), Decimal("0"))
        return subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @classmethod
    def nueva(cls, date: datetime | None = None) -> "Venta":
        return cls(
            id_venta=None,
            fecha=date or datetime.now(),
            total_price=Precio(Decimal("0")),
            detalles=[],
        )

    def agregar_detalle(self, detalle: "DetalleVenta") -> None:
        self._detalles.append(detalle)
        self.update_price()

    def update_price(self) -> None:
        self._total_price = Precio(self.total)

    def validar_no_vacia(self) -> None:
        if not self._detalles:
            raise EmptySaleError("No se puede registrar una venta sin productos.")

    @property
    def total_price(self) -> Precio:
        return self._total_price

    @property
    def detalles(self) -> list["DetalleVenta"]:
        return self._detalles

    def __repr__(self) -> str:
        return (
            f"Venta(id={self._id_venta!r}, fecha={self._fecha!r}, "
            f"total={self._total_price}, items={len(self._detalles)})"
        )
