from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.sqlalchemy.base import Base




class ProductoORM(Base):
    __tablename__ = 'Productos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    precio: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    detalle: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_de_barras: Mapped[str] = mapped_column(String(100), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

