from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.models.producto import Producto


@dataclass(frozen=True)
class ProductDTO:
    id_producto: int | None
    nombre: str
    codigo: str
    precio: Decimal
    precio_str: str
    detalle: str
    codigo_de_barras: str
    stock: int
    activo: bool

    @classmethod
    def from_domain(cls, producto: Producto) -> "ProductDTO":
        return cls(
            id_producto=producto.id_producto,
            nombre=producto.nombre,
            codigo=producto.codigo,
            precio=producto.precio.value,
            precio_str=str(producto.precio),
            detalle=producto.detalle,
            codigo_de_barras=producto.codigo_de_barras,
            stock=producto.stock.value,
            activo=producto.activo,
        )
