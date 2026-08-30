from __future__ import annotations

from decimal import Decimal

from app.domain.models.precio import Precio
from app.domain.models.producto import Producto
from app.domain.models.stock import Stock
from app.infrastructure.database.sqlalchemy.models.producto_orm import ProductoORM


class ProductoMapper:
    @staticmethod
    def to_domain_producto(row: ProductoORM) -> Producto:
        raw_price = Decimal(row.precio) if row.precio is not None else Decimal("0.00")
        safe_price = raw_price if raw_price >= Decimal("0") else Decimal("0.00")
        safe_stock = int(row.stock) if row.stock is not None else 0
        return Producto.from_persistence(
            id_producto=row.id,
            nombre=row.nombre,
            codigo=row.codigo,
            precio=Precio(safe_price),
            detalle=row.detalle or "",
            codigo_de_barras=row.codigo_de_barras or "",
            stock=Stock(safe_stock),
            activo=bool(getattr(row, "activo", True)),
        )

    @staticmethod
    def to_orm_producto(product: Producto) -> ProductoORM:
        return ProductoORM(
            id=product.id_producto,
            nombre=product.nombre,
            codigo=product.codigo,
            precio=product.precio.value,
            detalle=product.detalle,
            codigo_de_barras=product.codigo_de_barras,
            stock=product.stock.value,
            activo=product.activo,
        )

    @staticmethod
    def new_to_orm_producto(product: Producto) -> ProductoORM:
        return ProductoORM(
            nombre=product.nombre,
            codigo=product.codigo,
            precio=product.precio.value,
            detalle=product.detalle,
            codigo_de_barras=product.codigo_de_barras,
            stock=product.stock.value,
            activo=product.activo,
        )
