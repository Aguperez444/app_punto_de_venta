from Config.config_files_persistance import ConfigFilesPersistence
from screeninfo import get_monitors

class CommonWindowInitController:
    def __init__(self):
        self.config_pointer = ConfigFilesPersistence()
        self.icon_path = self.config_pointer.encontrar_ruta_icono()
        self.version = self.config_pointer.program_version
        self.theme = self.config_pointer.obtener_tema()

    @staticmethod
    def calculate_window_resolution():
        monitores = get_monitors()
        ancho = int(monitores[0].width // 1.3)
        alto = int(monitores[0].height // 1.3)
        x = (monitores[0].width - ancho) // 2
        y = (monitores[0].height - alto) // 2
        return f'{ancho}x{alto}+{x}+{y}'


    @staticmethod
    def calculate_popup_resolution():
        monitores = get_monitors()
        ancho = int(monitores[0].width // 2)
        alto = int(monitores[0].height // 1.5)
        x = (monitores[0].width - ancho) // 2
        y = (monitores[0].height - alto) // 2
        return f'{ancho}x{alto}+{x}+{y}'


    @staticmethod
    def get_screen_resolution():
        monitores = get_monitors()
        ancho = int(monitores[0].width // 1.3)
        alto = int(monitores[0].height // 1.3)
        return [ancho, alto]


    def obtener_tema_actual(self):
        return self.config_pointer.obtener_tema()


    def get_icon_path(self):
        return self.icon_path


    def get_version(self):
        return self.version


    def tema_cambiado(self, nuevo):
        self.config_pointer.cambiar_tema_config(nuevo)


