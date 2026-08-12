from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.precio import Precio
from app.domain.models.venta import Venta


@dataclass(frozen=True)
class SaleItemDTO:
    producto_id: int
    producto_nombre: str
    producto_codigo: str
    cantidad: int
    precio_unitario: Decimal
    precio_unitario_str: str
    subtotal: Decimal
    subtotal_str: str

    @classmethod
    def from_domain(cls, detalle: DetalleVenta) -> "SaleItemDTO":
        nombre = detalle.producto.nombre if detalle.producto else f"Producto #{detalle.producto_id}"
        codigo = detalle.producto.codigo if detalle.producto else "-"
        subtotal = detalle.calcular_subtotal()
        return cls(
            producto_id=detalle.producto_id,
            producto_nombre=nombre,
            producto_codigo=codigo,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario_actual.value,
            precio_unitario_str=str(detalle.precio_unitario_actual),
            subtotal=subtotal,
            subtotal_str=str(Precio(subtotal)),
        )


@dataclass(frozen=True)
class SaleSummaryDTO:
    venta_id: int | None
    fecha: datetime
    fecha_str: str
    hora_str: str
    resumen_productos: str
    cantidad_total: int
    items_count: int
    total: Decimal
    total_str: str

    @classmethod
    def from_domain(cls, venta: Venta) -> "SaleSummaryDTO":
        items_count = len(venta.detalles)
        cantidad_total = sum(d.cantidad for d in venta.detalles)
        if items_count == 0:
            resumen = "(Sin ítems)"
        elif items_count == 1:
            first = venta.detalles[0]
            resumen = first.producto.nombre if first.producto else f"Producto #{first.producto_id}"
        else:
            first = venta.detalles[0]
            first_name = (
                first.producto.nombre if first.producto else f"Producto #{first.producto_id}"
            )
            resumen = f"{first_name} (+{items_count - 1} más)"

        return cls(
            venta_id=venta.id_venta,
            fecha=venta.fecha,
            fecha_str=venta.fecha.strftime("%d/%m/%Y"),
            hora_str=venta.fecha.strftime("%H:%M:%S"),
            resumen_productos=resumen,
            cantidad_total=cantidad_total,
            items_count=items_count,
            total=venta.total_price.value,
            total_str=str(venta.total_price),
        )


@dataclass(frozen=True)
class SaleDetailDTO:
    venta_id: int | None
    fecha: datetime
    fecha_str: str
    hora_str: str
    total: Decimal
    total_str: str
    items: list[SaleItemDTO]

    @classmethod
    def from_domain(cls, venta: Venta) -> "SaleDetailDTO":
        return cls(
            venta_id=venta.id_venta,
            fecha=venta.fecha,
            fecha_str=venta.fecha.strftime("%d/%m/%Y"),
            hora_str=venta.fecha.strftime("%H:%M:%S"),
            total=venta.total_price.value,
            total_str=str(venta.total_price),
            items=[SaleItemDTO.from_domain(d) for d in venta.detalles],
        )
