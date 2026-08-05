from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_DEFAULT_THEME = "journal"
_PROGRAM_VERSION = "2.0.0"


class ConfigFilesPersistence:
    """Gestiona la configuración local en config.json con migración automática desde config.txt."""

    def __init__(self, base_dir: Path | str | None = None) -> None:
        self._program_version = _PROGRAM_VERSION
        if base_dir is None:
            self._ruta_documents_catalogo = self.get_ruta_documents()
        else:
            path = Path(base_dir)
            path.mkdir(parents=True, exist_ok=True)
            self._ruta_documents_catalogo = str(path)
        self._ruta_config = self.get_ruta_config_file()
        self._legacy_config = os.path.join(self._ruta_documents_catalogo, "config.txt")

    # region SETTERS AND GETTERS
    @property
    def ruta_documents_catalogo(self) -> str:
        return self._ruta_documents_catalogo

    @ruta_documents_catalogo.setter
    def ruta_documents_catalogo(self, value: str) -> None:
        self._ruta_documents_catalogo = value

    @property
    def ruta_config(self) -> str:
        return self._ruta_config

    @ruta_config.setter
    def ruta_config(self, value: str) -> None:
        self._ruta_config = value

    @property
    def program_version(self) -> str:
        return self._program_version

    # endregion

    @staticmethod
    def get_ruta_documents() -> str:
        """
        Obtiene la ruta a la carpeta de Documentos del usuario respetando la localización (XDG en Linux)
        y crea la subcarpeta 'catalogo' si no existe.
        """
        home = os.path.expanduser("~")
        docs = None

        if sys.platform.startswith("linux"):
            try:
                out = subprocess.check_output(
                    ["xdg-user-dir", "DOCUMENTS"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                ).strip()
                if out and out != "$HOME":
                    docs = out
            except Exception as e:
                logger.debug("No se pudo ejecutar xdg-user-dir: %s", e)

            if not docs:
                config_path = os.path.join(home, ".config", "user-dirs.dirs")
                try:
                    with open(config_path, "rt", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("XDG_DOCUMENTS_DIR"):
                                value = line.split("=", 1)[1].strip().strip('"')
                                docs = value.replace("$HOME", home)
                                break
                except Exception as e:
                    logger.debug("No se pudo leer user-dirs.dirs: %s", e)

            if not docs:
                docs = os.path.join(home, "Documents")
        else:
            docs = os.path.join(home, "Documents")

        ruta_carpeta = os.path.join(docs, "catalogo")
        os.makedirs(ruta_carpeta, exist_ok=True)
        return ruta_carpeta

    @staticmethod
    def encontrar_ruta_icono() -> str:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_path = Path(getattr(sys, "_MEIPASS"))
        else:
            # app/infrastructure/config/config_files_persistance.py -> app/infrastructure/resources/static
            base_path = Path(__file__).resolve().parents[1] / "resources" / "static"

        return str(base_path / "program_icon.png")

    def get_ruta_config_file(self) -> str:
        return os.path.join(self._ruta_documents_catalogo, "config.json")

    def _default_config(self) -> dict:
        return {
            "theme": _DEFAULT_THEME,
            "database_url": "",
        }

    def _migrate_legacy_if_needed(self) -> dict | None:
        legacy_path = Path(self._legacy_config)
        if not legacy_path.exists():
            return None
        try:
            lines = [line.strip() for line in legacy_path.read_text(encoding="utf-8").splitlines()]
            theme = lines[0] if len(lines) > 0 and lines[0] else _DEFAULT_THEME
            db_url = lines[1] if len(lines) > 1 and lines[1] != theme else ""
            data = {"theme": theme, "database_url": db_url}
            self._write_config(data)
            logger.info("Configuración migrada automáticamente de config.txt a config.json")
            return data
        except OSError as e:
            logger.warning("No se pudo migrar config.txt: %s", e)
            return None

    def _read_config(self) -> dict:
        cfg_path = Path(self._ruta_config)
        if not cfg_path.exists():
            migrated = self._migrate_legacy_if_needed()
            if migrated is not None:
                return migrated
            return self._default_config()

        try:
            raw = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                merged = self._default_config()
                merged.update(raw)
                return merged
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("config.json inválido, usando valores por defecto: %s", e)
        return self._default_config()

    def _write_config(self, data: dict) -> None:
        cfg_path = Path(self._ruta_config)
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = cfg_path.with_suffix(".json.tmp")
        tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp_path, cfg_path)
        try:
            os.chmod(cfg_path, 0o600)
        except OSError:
            pass

    def get_ruta_bdd(self) -> str:
        env_url = os.getenv("DATABASE_URL")
        if env_url and env_url.strip():
            return env_url.strip()
        data = self._read_config()
        return str(data.get("database_url", "")).strip()

    def set_new_bbd_route_in_config(self, ruta_new: str) -> None:
        data = self._read_config()
        data["database_url"] = ruta_new.strip()
        self._write_config(data)

    def is_first_time_running(self) -> bool:
        if os.getenv("DATABASE_URL", "").strip():
            return False
        cfg_path = Path(self._ruta_config)
        if not cfg_path.exists():
            migrated = self._migrate_legacy_if_needed()
            if migrated and migrated.get("database_url"):
                return False
            self._write_config(self._default_config())
            return True
        return not bool(self.get_ruta_bdd())

    def obtener_tema(self) -> str:
        data = self._read_config()
        return str(data.get("theme") or _DEFAULT_THEME)

    def cambiar_tema_config(self, new_tema: str) -> None:
        data = self._read_config()
        data["theme"] = new_tema.strip() or _DEFAULT_THEME
        self._write_config(data)
