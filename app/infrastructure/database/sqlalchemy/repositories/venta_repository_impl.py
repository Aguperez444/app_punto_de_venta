from __future__ import annotations

from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.application.ports.sale_repository import ISaleRepository
from app.domain.models.venta import Venta
from app.infrastructure.database.sqlalchemy.mappers.venta_mapper import VentaMapper
from app.infrastructure.database.sqlalchemy.models.venta_orm import VentaORM


class SaleRepositoryImpl(ISaleRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_ventas_by_date(self, initial_date: datetime, final_date: datetime) -> list[Venta]:
        stmt = (
            select(VentaORM)
            .where(and_(VentaORM.fecha >= initial_date, VentaORM.fecha < final_date))
            .order_by(VentaORM.fecha.desc(), VentaORM.id.desc())
        )
        found = self.session.scalars(stmt).unique().all()
        return [VentaMapper.to_domain_venta(venta_orm) for venta_orm in found]

    def get_by_id(self, venta_id: int) -> Venta | None:
        found = self.session.get(VentaORM, venta_id)
        if found is None:
            return None
        return VentaMapper.to_domain_venta(found)

    def save_new(self, venta: Venta) -> None:
        venta_orm = VentaMapper.new_to_orm_venta(venta)
        self.session.add(venta_orm)
        self.session.flush()
        venta.id_venta = venta_orm.id
