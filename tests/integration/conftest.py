import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.sqlalchemy.base import Base
import app.infrastructure.database.sqlalchemy.models  # noqa: F401
from app.infrastructure.database.sqlalchemy.models.detalle_venta_orm import DetalleVentaORM
from app.infrastructure.database.sqlalchemy.models.producto_orm import ProductoORM
from app.infrastructure.database.sqlalchemy.models.venta_orm import VentaORM
from app.infrastructure.database.sqlalchemy.unit_of_work.unit_of_work_impl import SqlAlchemyUnitOfWork

pytestmark = pytest.mark.integration


@pytest.fixture(scope="session")
def engine(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("db") / "test_integration.sqlite"
    engine = create_engine(f"sqlite:///{db_path}", echo=False, future=True)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def session_factory(engine):
    return sessionmaker(bind=engine, future=True)


@pytest.fixture(autouse=True)
def _clean_tables(session_factory):
    """Aisla cada test de integración limpiando las tablas antes de ejecutarlo."""
    with session_factory() as session:
        session.execute(delete(DetalleVentaORM))
        session.execute(delete(VentaORM))
        session.execute(delete(ProductoORM))
        session.commit()


@pytest.fixture()
def uow_factory_integration(session_factory):
    def factory():
        return SqlAlchemyUnitOfWork(session_factory)
    return factory
