from app.domain.models.venta import Venta
from app.domain.models.precio import Precio

from app.infrastructure.database.sqlalchemy.mappers.detalle_venta_mapper import DetalleVentaMapper

from app.infrastructure.database.sqlalchemy.models.venta_orm import VentaORM

class VentaMapper:
    @staticmethod
    def to_domain_venta(row: VentaORM) -> Venta:
        return Venta(
            id_venta=row.id,
            fecha=row.fecha,
            total_price=Precio(row.total_price),
            detalles=[DetalleVentaMapper.to_domain_detalle_venta(detalle) for detalle in row.detalles]
        )

    @staticmethod
    def to_orm_venta(row: Venta) -> VentaORM:
        return VentaORM(
            id=row.id_venta,
            fecha=row.fecha,
            total_price=row.total_price.value,
            detalles=[DetalleVentaMapper.to_orm_detalle_venta(detalle) for detalle in row.detalles]
        )

    @staticmethod
    def new_to_orm_venta(row: Venta) -> VentaORM:
        return VentaORM(
            fecha=row.fecha,
            total_price=row.total_price.value,
            detalles=[DetalleVentaMapper.to_orm_detalle_venta(detalle) for detalle in row.detalles]
        )
