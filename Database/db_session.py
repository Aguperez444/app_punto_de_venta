# /persistence/db_session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from Config.config_files_persistance import ConfigFilesPersistence

config = ConfigFilesPersistence()

DATABASE_URL = f"sqlite:///{config.get_ruta_bdd()}"

config = None

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
