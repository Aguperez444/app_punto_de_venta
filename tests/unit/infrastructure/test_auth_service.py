import pytest

from app.domain.custom_errors import DomainValidationError
from app.infrastructure.config.auth_service import AuthService


@pytest.mark.unit
def test_auth_service_set_and_verify_password(tmp_path, monkeypatch):
    monkeypatch.delenv("APP_ADMIN_PASSWORD", raising=False)
    auth = AuthService(credentials_path=tmp_path / "auth.json")

    assert auth.is_password_configured() is False
    assert auth.verify_password("cualquiera") is False

    auth.set_password("farmacia2026")

    assert auth.is_password_configured() is True
    assert auth.verify_password("farmacia2026") is True
    assert auth.verify_password("incorrecta") is False
    assert auth.verify_password("") is False

    raw = (tmp_path / "auth.json").read_text(encoding="utf-8")
    assert "farmacia2026" not in raw
    assert "scrypt" in raw


@pytest.mark.unit
def test_auth_service_rejects_short_password(tmp_path, monkeypatch):
    monkeypatch.delenv("APP_ADMIN_PASSWORD", raising=False)
    auth = AuthService(credentials_path=tmp_path / "auth.json")

    with pytest.raises(DomainValidationError):
        auth.set_password("123")


@pytest.mark.unit
def test_auth_service_change_password(tmp_path, monkeypatch):
    monkeypatch.delenv("APP_ADMIN_PASSWORD", raising=False)
    auth = AuthService(credentials_path=tmp_path / "auth.json")
    auth.set_password("clave_inicial")

    with pytest.raises(DomainValidationError):
        auth.change_password("incorrecta", "clave_nueva")

    auth.change_password("clave_inicial", "clave_nueva")
    assert auth.verify_password("clave_inicial") is False
    assert auth.verify_password("clave_nueva") is True


@pytest.mark.unit
def test_auth_service_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_ADMIN_PASSWORD", "env_secret")
    auth = AuthService(credentials_path=tmp_path / "auth.json")

    assert auth.is_password_configured() is True
    assert auth.verify_password("env_secret") is True
    assert auth.verify_password("other") is False
