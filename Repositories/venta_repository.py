from datetime import datetime

from sqlalchemy import and_

from Database.db_session import SessionLocal
from Models.Venta import Venta

class VentaRepository:
    @staticmethod
    def save_venta(venta: Venta):
        with SessionLocal() as session:
            try:
                session.add(venta)
                session.commit()
                session.refresh(venta)
            except Exception:
                session.rollback()
                raise

    @staticmethod
    def find_ventas_by_date(initial_date: datetime, final_date: datetime) -> list[Venta]:

        with SessionLocal() as session:

            return (
                session.query(Venta)
                .filter(and_(Venta.fecha >= initial_date, Venta.fecha < final_date))
                .all()
            )

    @staticmethod
    def update_venta_total_price(venta: Venta, new_total_price: float):
        with SessionLocal() as session:
            try:
                venta_in_db = session.query(Venta).get(venta.id)
                if venta_in_db:
                    venta_in_db.total_price = new_total_price
                    session.commit()
                else:
                    raise ValueError(f'Venta con id {venta.id} no encontrada.')
            except Exception:
                session.rollback()
                raise

    @staticmethod
    def update_venta(venta: Venta):
        with SessionLocal() as session:
            try:
                venta_in_db = session.query(Venta).get(venta.id)
                if venta_in_db:
                    venta_in_db.fecha = venta.fecha
                    venta_in_db.total_price = venta.total_price
                    venta_in_db.detalles = venta.detalles
                    session.commit()
                else:
                    raise ValueError(f'Venta con id {venta.id} no encontrada.')
            except Exception:
                session.rollback()
                raise