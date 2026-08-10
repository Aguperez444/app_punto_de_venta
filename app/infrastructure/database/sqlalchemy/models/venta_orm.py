from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Index, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.sqlalchemy.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.sqlalchemy.models.detalle_venta_orm import DetalleVentaORM


class VentaORM(Base):
    __tablename__ = "Ventas"
    __table_args__ = (
        CheckConstraint("total_price >= 0", name="ck_ventas_total_no_negativo"),
        Index("ix_ventas_fecha", "fecha"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )

    detalles: Mapped[list["DetalleVentaORM"]] = relationship(
        back_populates="venta",
        cascade="all, delete-orphan",
        lazy="joined",
    )
