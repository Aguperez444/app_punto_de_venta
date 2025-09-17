# Models/venta.py

from sqlalchemy import Column, Integer, Numeric, DateTime
from sqlalchemy.orm import relationship

from Database.db_session import Base

class Venta(Base):
    __tablename__ = 'Ventas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=True)   # o DateTime si querés manejarlo como fecha real
    total_price = Column(Numeric, nullable=True)

    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan", lazy='joined')

    def __repr__(self):
        return f"<Venta(id={self.id}, fecha='{self.fecha}', total_price={self.total_price})>"

