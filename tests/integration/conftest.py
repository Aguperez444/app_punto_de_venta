import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.sqlalchemy.base import Base
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


@pytest.fixture()
def uow_factory_integration(session_factory):
    def factory():
        return SqlAlchemyUnitOfWork(session_factory)
    return factory
