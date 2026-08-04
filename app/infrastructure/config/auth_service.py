from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path

from app.domain.custom_errors import DomainValidationError


class AuthService:
    """Gestiona la contraseña administrativa usando scrypt con salt aleatorio."""

    _SCRYPT_N = 2**14
    _SCRYPT_R = 8
    _SCRYPT_P = 1
    _DKLEN = 32
    _MIN_LENGTH = 4

    def __init__(self, credentials_path: Path | str | None = None) -> None:
        if credentials_path is None:
            from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence

            base_dir = Path(ConfigFilesPersistence.get_ruta_documents())
            self._path = base_dir / "auth.json"
        else:
            self._path = Path(credentials_path)

    @property
    def credentials_path(self) -> Path:
        return self._path

    def is_password_configured(self) -> bool:
        if os.getenv("APP_ADMIN_PASSWORD"):
            return True
        return self._read_record() is not None

    def set_password(self, new_password: str) -> None:
        if not isinstance(new_password, str) or len(new_password.strip()) < self._MIN_LENGTH:
            raise DomainValidationError(
                f"La contraseña debe tener al menos {self._MIN_LENGTH} caracteres."
            )
        salt_hex = secrets.token_hex(16)
        digest_hex = self._derive_key(new_password, salt_hex)
        payload = {
            "algorithm": "scrypt",
            "n": self._SCRYPT_N,
            "r": self._SCRYPT_R,
            "p": self._SCRYPT_P,
            "salt": salt_hex,
            "hash": digest_hex,
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        try:
            os.chmod(self._path, 0o600)
        except OSError:
            pass

    def verify_password(self, candidate: str) -> bool:
        if not isinstance(candidate, str) or not candidate:
            return False

        env_password = os.getenv("APP_ADMIN_PASSWORD")
        if env_password:
            return hmac.compare_digest(candidate, env_password)

        record = self._read_record()
        if record is None:
            return False

        salt_hex = record.get("salt")
        expected_hash = record.get("hash")
        if not salt_hex or not expected_hash:
            return False

        derived = self._derive_key(
            candidate,
            salt_hex,
            n=int(record.get("n", self._SCRYPT_N)),
            r=int(record.get("r", self._SCRYPT_R)),
            p=int(record.get("p", self._SCRYPT_P)),
        )
        return hmac.compare_digest(derived, expected_hash)

    def change_password(self, current_password: str, new_password: str) -> None:
        if self.is_password_configured() and not self.verify_password(current_password):
            raise DomainValidationError("La contraseña actual es incorrecta.")
        self.set_password(new_password)

    def _read_record(self) -> dict | None:
        if not self._path.exists():
            return None
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "salt" in data and "hash" in data:
                return data
        except (OSError, json.JSONDecodeError):
            return None
        return None

    def _derive_key(
        self,
        password: str,
        salt_hex: str,
        *,
        n: int | None = None,
        r: int | None = None,
        p: int | None = None,
    ) -> str:
        dk = hashlib.scrypt(
            password.encode("utf-8"),
            salt=bytes.fromhex(salt_hex),
            n=n or self._SCRYPT_N,
            r=r or self._SCRYPT_R,
            p=p or self._SCRYPT_P,
            dklen=self._DKLEN,
        )
        return dk.hex()
