from __future__ import annotations

import os
import sys
from logging.config import fileConfig

from alembic import context

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _no_drop_extras(object, name, type_, reflected, compare_to):
    if reflected and compare_to is None:
        return False
    return True


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.infrastructure.database.sqlalchemy.base import Base
import app.infrastructure.database.sqlalchemy.models  # noqa: F401
from app.infrastructure.database.sqlalchemy.engine_factory import create_db_engine

target_metadata = Base.metadata


def _resolve_db_url() -> str | None:
    x_args = context.get_x_argument(as_dictionary=True)
    if x_args.get("db_url"):
        return x_args["db_url"]
    env_url = os.getenv("DATABASE_URL")
    if env_url and env_url.strip():
        return env_url.strip()
    ini_url = config.get_main_option("sqlalchemy.url")
    if ini_url and "driver://user:pass" not in ini_url:
        return ini_url
    return None


def run_migrations_offline() -> None:
    engine = create_db_engine(db_url=_resolve_db_url())
    url = engine.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        include_object=_no_drop_extras,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_db_engine(db_url=_resolve_db_url())

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_object=_no_drop_extras,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
