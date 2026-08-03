from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

_CONFIGURED = False
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging(log_dir: Path | str | None = None, level: str | None = None) -> Path:
    """Configura logging rotativo a archivo y salida a consola para toda la aplicación."""
    global _CONFIGURED

    env_level = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    numeric_level = getattr(logging, env_level, logging.INFO)

    if log_dir is None:
        from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence

        base_dir = Path(ConfigFilesPersistence.get_ruta_documents()) / "logs"
    else:
        base_dir = Path(log_dir)

    base_dir.mkdir(parents=True, exist_ok=True)
    log_file = base_dir / "app.log"

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    if not _CONFIGURED:
        formatter = logging.Formatter(_LOG_FORMAT)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(numeric_level)

        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(numeric_level)

        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        _install_global_excepthook()
        _CONFIGURED = True

    return log_file


def reset_logging_configuration() -> None:
    """Reinicia el estado de logging (útil en tests)."""
    global _CONFIGURED
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        handler.close()
        root_logger.removeHandler(handler)
    _CONFIGURED = False


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def _install_global_excepthook() -> None:
    logger = logging.getLogger("app.uncaught")

    def _handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Excepción no controlada", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = _handle_exception
