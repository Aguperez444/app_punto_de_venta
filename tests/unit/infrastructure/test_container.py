import pytest

from app.infrastructure.config.auth_service import AuthService
from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence
from app.infrastructure.database.sqlalchemy.base import Base
from app.infrastructure.di.container import AppContainer


@pytest.mark.unit
def test_container_lazy_engine_and_reload(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    cfg = ConfigFilesPersistence(base_dir=tmp_path)
    db1 = tmp_path / "one.db"
    db2 = tmp_path / "two.db"
    cfg.set_new_bbd_route_in_config(f"sqlite:///{db1}")

    container = AppContainer(
        config=cfg,
        auth_service=AuthService(credentials_path=tmp_path / "auth.json"),
    )
    try:
        # No crea engine hasta acceder a uow_factory
        assert container._engine is None
        uow_factory = container.uow_factory
        assert container._engine is not None
        Base.metadata.create_all(container._engine)

        with uow_factory() as uow:
            assert uow.product_repo.list_products() == []

        container.reload_database(f"sqlite:///{db2}")
        assert container._engine is None
        assert cfg.get_ruta_bdd() == f"sqlite:///{db2}"
    finally:
        container.close()
