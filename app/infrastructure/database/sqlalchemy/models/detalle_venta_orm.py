from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.infrastructure.database.sqlalchemy.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.database.sqlalchemy.models.producto_orm import ProductoORM
    from app.infrastructure.database.sqlalchemy.models.venta_orm import VentaORM

class DetalleVentaORM(Base):
    __tablename__ = 'Detalle_venta'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_venta: Mapped[int] = mapped_column(ForeignKey("Ventas.id", ondelete="CASCADE"), nullable=False)
    id_producto: Mapped[int] = mapped_column(ForeignKey("Productos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario_actual: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    venta: Mapped['VentaORM'] = relationship(back_populates="detalles", lazy="joined")

    producto: Mapped['ProductoORM'] = relationship(lazy="joined")


