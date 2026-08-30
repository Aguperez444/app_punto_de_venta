from __future__ import annotations

from screeninfo import get_monitors

from app.infrastructure.config.config_files_persistance import ConfigFilesPersistence


class CommonWindowInitController:
    def __init__(self, config_persistence: ConfigFilesPersistence | None = None):
        self.config_pointer = config_persistence or ConfigFilesPersistence()
        self.icon_path = self.config_pointer.encontrar_ruta_icono()
        self.version = self.config_pointer.program_version
        self.theme = self.config_pointer.obtener_tema()

    @staticmethod
    def calculate_window_resolution() -> str:
        monitores = get_monitors()
        ancho = int(monitores[0].width // 1.3)
        alto = int(monitores[0].height // 1.3)
        x = (monitores[0].width - ancho) // 2
        y = (monitores[0].height - alto) // 2
        return f"{ancho}x{alto}+{x}+{y}"

    @staticmethod
    def calculate_centered_geometry(
        parent_window, width: int, height: int
    ) -> str:
        """Calcula geometría WxH+X+Y centrada sobre `parent_window` en su monitor actual."""
        parent_window.update_idletasks()
        parent_x = parent_window.winfo_rootx()
        parent_y = parent_window.winfo_rooty()
        parent_width = max(parent_window.winfo_width(), 1)
        parent_height = max(parent_window.winfo_height(), 1)

        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        return f"{width}x{height}+{x}+{y}"

    @staticmethod
    def calculate_popup_resolution(
        parent_window, width: int | None = None, height: int | None = None
    ) -> str:
        parent_window.update_idletasks()
        parent_width = max(parent_window.winfo_width(), 800)
        parent_height = max(parent_window.winfo_height(), 600)

        ancho = width if width is not None else min(max(int(parent_width * 0.62), 820), 1150)
        alto = height if height is not None else min(max(int(parent_height * 0.62), 540), 720)

        return CommonWindowInitController.calculate_centered_geometry(
            parent_window, ancho, alto
        )

    @staticmethod
    def center_window_on_parent(window, parent_window, width: int, height: int) -> None:
        """Asocia `window` como transient del padre y la centra en el mismo monitor."""
        try:
            window.transient(parent_window)
        except Exception:
            pass
        geom = CommonWindowInitController.calculate_centered_geometry(
            parent_window, width, height
        )
        window.geometry(geom)

    @staticmethod
    def get_screen_resolution() -> list[int]:
        monitores = get_monitors()
        ancho = int(monitores[0].width // 1.3)
        alto = int(monitores[0].height // 1.3)
        return [ancho, alto]

    def obtener_tema_actual(self) -> str:
        return self.config_pointer.obtener_tema()

    def get_icon_path(self) -> str:
        return self.icon_path

    def get_version(self) -> str:
        return self.version

    def tema_cambiado(self, nuevo: str) -> None:
        self.config_pointer.cambiar_tema_config(nuevo)
