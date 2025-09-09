from Persistence.db_session import SessionLocal
from Models.DetalleVenta import DetalleVenta

class DetalleRepository:
    @staticmethod
    def save_detalle(detalle: DetalleVenta):
        with SessionLocal() as session:
            try:
                session.add(detalle)
                session.commit()
                session.refresh(detalle)
            except Exception:
                session.rollback()
                raise
