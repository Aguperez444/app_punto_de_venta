from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, Numeric, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.infrastructure.database.sqlalchemy.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.database.sqlalchemy.models.detalle_venta_orm import DetalleVentaORM


class VentaORM(Base):
    __tablename__ = 'Ventas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False, default=0.0)

    detalles: Mapped[list['DetalleVentaORM']] = relationship(
        back_populates="venta",
        cascade="all, delete-orphan",
        lazy="joined",
    )

