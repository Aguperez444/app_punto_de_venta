from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.application.ports.sale_repository import ISaleRepository
from app.domain.models.venta import Venta

from app.infrastructure.database.sqlalchemy.models.venta_orm import VentaORM
from app.infrastructure.database.sqlalchemy.mappers.venta_mapper import VentaMapper


class SaleRepositoryImpl(ISaleRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_ventas_by_date(self, initial_date: datetime, final_date: datetime) -> list[Venta] | list:


        found = (
            self.session.query(VentaORM)
            .filter(and_(VentaORM.fecha >= initial_date, VentaORM.fecha < final_date))
            .all()
        )

        if found:
            # el typechecker detecta mal lo que devuelve el query().all()
            # noinspection PyTypeChecker
            return [VentaMapper.to_domain_venta(venta_orm) for venta_orm in found]
        return []


    def save_new(self, venta: Venta) -> None:
        venta_orm = VentaMapper.new_to_orm_venta(venta)  # copia fecha, total y detalles
        self.session.add(venta_orm)
        self.session.flush()               # obtenemos id de la DB
        print(f"VENTA ID EN EL REPO: {venta_orm.id}\n\n\n\n")
        venta.id_venta = venta_orm.id                       # propagamos id al dominio


