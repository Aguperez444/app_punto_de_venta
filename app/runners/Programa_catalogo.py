import logging

from app.infrastructure.config.logging_config import configure_logging
from app.infrastructure.di.container import AppContainer
from app.infrastructure.ui.tkinter.controllers.common.program_start_controller import (
    ProgramStartController,
)

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    container = AppContainer()

    program_start_controller = ProgramStartController(config_persistence=container.config)
    program_start_controller.verify_first_run()

    ok, msg = container.ensure_database_schema()
    if not ok:
        logger.error("No se pudo actualizar automáticamente el esquema de la BDD: %s", msg)

    from app.infrastructure.ui.tkinter.views.windows.main_menu_window import MainMenuWindow

    main_window = MainMenuWindow(container=container)
    try:
        main_window.mainloop()
    finally:
        container.close()


if __name__ == "__main__":
    main()
