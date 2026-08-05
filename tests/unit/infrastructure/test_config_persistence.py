from pathlib import Path
import pytest

from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence


@pytest.mark.unit
def test_config_first_run_and_persist_db_url(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    cfg = ConfigFilesPersistence(base_dir=tmp_path)

    assert cfg.is_first_time_running() is True
    assert cfg.obtener_tema() == "journal"
    assert cfg.get_ruta_bdd() == ""

    cfg.set_new_bbd_route_in_config("postgresql+psycopg://user:pass@localhost:5432/farma")
    assert cfg.is_first_time_running() is False
    assert cfg.get_ruta_bdd() == "postgresql+psycopg://user:pass@localhost:5432/farma"

    cfg.cambiar_tema_config("darkly")
    assert cfg.obtener_tema() == "darkly"
    assert cfg.get_ruta_bdd() == "postgresql+psycopg://user:pass@localhost:5432/farma"


@pytest.mark.unit
def test_config_migrates_legacy_txt_file(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    legacy = tmp_path / "config.txt"
    legacy.write_text("darkly\npostgresql+psycopg://u:p@127.0.0.1:5432/db\n", encoding="utf-8")

    cfg = ConfigFilesPersistence(base_dir=tmp_path)

    assert cfg.is_first_time_running() is False
    assert cfg.obtener_tema() == "darkly"
    assert cfg.get_ruta_bdd() == "postgresql+psycopg://u:p@127.0.0.1:5432/db"
    assert (tmp_path / "config.json").exists()


@pytest.mark.unit
def test_config_env_var_overrides_database_url(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///env_override.db")
    cfg = ConfigFilesPersistence(base_dir=tmp_path)

    assert cfg.is_first_time_running() is False
    assert cfg.get_ruta_bdd() == "sqlite:///env_override.db"


@pytest.mark.unit
def test_icon_path_resolves_to_existing_file():
    icon = Path(ConfigFilesPersistence.encontrar_ruta_icono())
    assert icon.name == "program_icon.png"
    assert icon.exists()
