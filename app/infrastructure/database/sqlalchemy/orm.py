from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base

from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.producto import Producto
from app.domain.models.venta import Venta
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock

Base = declarative_base()

class ProductoORM(Base):
    __tablename__ = 'Productos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    detalle: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_de_barras: Mapped[str] = mapped_column(String(100), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class VentaORM(Base):
    __tablename__ = 'Ventas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False, default=0.0)

    # Relación 1→N con detalles
    detalles: Mapped[list["DetalleVentaORM"]] = relationship(
        back_populates="venta",
        cascade="all, delete-orphan",
        lazy="joined",
    )


class DetalleVentaORM(Base):
    __tablename__ = 'Detalle_venta'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_venta: Mapped[int] = mapped_column(ForeignKey("Ventas.id", ondelete="CASCADE"), nullable=False)
    id_producto: Mapped[int] = mapped_column(ForeignKey("Productos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario_actual: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    venta: Mapped[VentaORM] = relationship(back_populates="detalles", lazy="joined")

    producto: Mapped[ProductoORM] = relationship(lazy="joined")


# region Mappers
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

# endregion
