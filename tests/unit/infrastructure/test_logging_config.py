import logging
import pytest

from app.infrastructure.config.logging_config import (
    configure_logging,
    get_logger,
    reset_logging_configuration,
)


@pytest.mark.unit
def test_configure_logging_writes_to_rotating_file(tmp_path):
    reset_logging_configuration()
    try:
        log_file = configure_logging(log_dir=tmp_path, level="INFO")
        logger = get_logger("tests.logging_check")
        logger.info("Mensaje de prueba estructurado")

        for handler in logging.getLogger().handlers:
            handler.flush()

        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "Mensaje de prueba estructurado" in content
        assert "INFO" in content
    finally:
        reset_logging_configuration()
