import pytest

from app.infrastructure.database.sqlalchemy.engine_factory import (
    test_db_connection as check_db_connection,
)
from app.infrastructure.ui.tkinter.views.windows.find_bdd_window import build_postgres_url


@pytest.mark.unit
def test_build_postgres_url_escapes_credentials():
    url = build_postgres_url("192.168.1.10", "5432", "farmacia", "admin", "p@ss/123")
    assert url == "postgresql+psycopg://admin:p%40ss%2F123@192.168.1.10:5432/farmacia"


@pytest.mark.unit
def test_build_postgres_url_requires_host_db_user():
    with pytest.raises(ValueError):
        build_postgres_url("", "5432", "farmacia", "admin", "1234")


@pytest.mark.unit
def test_db_connection_helper_sqlite(tmp_path):
    db_file = tmp_path / "conn_check.db"
    ok, msg = check_db_connection(f"sqlite:///{db_file}")
    assert ok is True
    assert "exitosa" in msg.lower()

    ok_bad, _ = check_db_connection("")
    assert ok_bad is False
