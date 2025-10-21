from __future__ import annotations

from app.domain.models.producto import Producto
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock
from app.infrastructure.database.sqlalchemy.models.producto_orm import ProductoORM


class ProductoMapper:
    @staticmethod
    def to_domain_producto(row: ProductoORM) -> Producto:
        return Producto(
            id_producto=row.id,
            nombre=row.nombre,
            codigo=row.codigo,
            precio=Precio(row.precio),
            detalle=row.detalle,
            codigo_de_barras=row.codigo_de_barras,
            stock=Stock(row.stock)
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
            stock=product.stock.value
        )

    @staticmethod
    def new_to_orm_producto(product: Producto) -> ProductoORM:
        return ProductoORM(
            nombre=product.nombre,
            codigo=product.codigo,
            precio=product.precio.value,
            detalle=product.detalle,
            codigo_de_barras=product.codigo_de_barras,
            stock=product.stock.value
        )
