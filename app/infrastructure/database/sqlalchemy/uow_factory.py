from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence
from app.infrastructure.database.sqlalchemy.unit_of_work_impl import SqlAlchemyUnitOfWork

config = ConfigFilesPersistence()

#DATABASE_URL = f"sqlite:///{config.get_ruta_bdd()}"

DATABASE_URL = str(config.get_ruta_bdd())

config = None

#engine = create_engine(DATABASE_URL, echo=True)

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,    # 30 min
    echo=True,
    isolation_level="READ COMMITTED",
)


SessionLocal = sessionmaker(bind=engine)


def uow_factory() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(SessionLocal)