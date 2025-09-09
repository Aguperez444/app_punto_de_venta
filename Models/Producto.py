from sqlalchemy import Column, Integer, String, Float
from Persistence.db_session import Base


class Producto(Base):
    __tablename__ = 'Productos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String(100), nullable=False)
    codigo = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    detalle = Column(String(200), nullable=True)
    codigo_de_barras = Column(String(100), nullable=True)
    stock = Column(Integer, nullable=False)


    def __repr__(self):
        return (f"<Producto(id={self.id}, producto='{self.producto}', codigo='{self.codigo}', precio={self.precio},"
                f" detalle='{self.detalle}', codigo_de_barras='{self.codigo_de_barras}', stock={self.stock})>")
