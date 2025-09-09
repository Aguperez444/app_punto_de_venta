from decimal import Decimal

from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from Persistence.db_session import Base

class DetalleVenta(Base):
    __tablename__ = 'Detalle_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey("Ventas.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("Productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario_actual = Column(Numeric, nullable=False)

    # Relación inversa con Venta
    venta = relationship("Venta", back_populates="detalles")

    # Relación con Producto (si querés acceso directo al producto)
    producto = relationship("Producto")

    def calcular_subtotal(self) -> Decimal:
        return self.cantidad * self.precio_unitario_actual

    def __repr__(self):
        return (f"<DetalleVenta(id={self.id}, id_venta={self.id_venta}, "
                f"id_producto={self.id_producto}, cantidad={self.cantidad}, "
                f"precio_unitario_actual={self.precio_unitario_actual})>")