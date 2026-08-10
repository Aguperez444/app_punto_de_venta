from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Index, Integer, Numeric, String, true
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.sqlalchemy.base import Base


class ProductoORM(Base):
    __tablename__ = "Productos"
    __table_args__ = (
        CheckConstraint("precio >= 0", name="ck_productos_precio_no_negativo"),
        Index("ix_productos_nombre", "nombre"),
        Index("ix_productos_codigo", "codigo"),
        Index("ix_productos_codigo_de_barras", "codigo_de_barras"),
        Index("ix_productos_stock", "stock"),
        Index("ix_productos_activo", "activo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    detalle: Mapped[str | None] = mapped_column(String(255), nullable=True)
    codigo_de_barras: Mapped[str | None] = mapped_column(String(100), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=true()
    )
