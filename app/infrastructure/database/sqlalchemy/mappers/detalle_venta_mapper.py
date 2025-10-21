
from app.infrastructure.database.sqlalchemy.mappers.producto_mapper import ProductoMapper

from app.infrastructure.database.sqlalchemy.models.detalle_venta_orm import DetalleVentaORM

from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.precio import Precio




class DetalleVentaMapper:
    @staticmethod
    def to_domain_detalle_venta(row: DetalleVentaORM) -> DetalleVenta:
        return DetalleVenta(
            id_detalle=row.id,
            venta_id=row.id_venta,
            producto_id=row.id_producto,
            cantidad=row.cantidad,
            precio_unitario_actual=Precio(row.precio_unitario_actual),
            product=ProductoMapper.to_domain_producto(row.producto) if row.producto else None
        )

    @staticmethod
    def to_orm_detalle_venta(detalle: DetalleVenta) -> DetalleVentaORM:
        return DetalleVentaORM(
            id=detalle.id,
            id_venta=detalle.venta_id,
            id_producto=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario_actual=detalle.precio_unitario_actual.value
        )

    @staticmethod
    def new_to_orm_detalle_venta(detalle: DetalleVenta) -> DetalleVentaORM:
        return DetalleVentaORM(
            id_venta=detalle.venta_id,
            id_producto=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario_actual=detalle.precio_unitario_actual.value
        )