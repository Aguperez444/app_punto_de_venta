from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.sqlalchemy.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.sqlalchemy.models.producto_orm import ProductoORM
    from app.infrastructure.database.sqlalchemy.models.venta_orm import VentaORM


class DetalleVentaORM(Base):
    __tablename__ = "Detalle_venta"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_detalle_cantidad_positiva"),
        CheckConstraint("precio_unitario_actual >= 0", name="ck_detalle_precio_no_negativo"),
        Index("ix_detalle_venta_id_venta", "id_venta"),
        Index("ix_detalle_venta_id_producto", "id_producto"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_venta: Mapped[int] = mapped_column(
        ForeignKey("Ventas.id", ondelete="CASCADE"), nullable=False
    )
    id_producto: Mapped[int] = mapped_column(ForeignKey("Productos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario_actual: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    venta: Mapped["VentaORM"] = relationship(back_populates="detalles", lazy="select")
    producto: Mapped["ProductoORM"] = relationship(lazy="joined")
