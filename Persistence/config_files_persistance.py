import os
import sys

class ConfigFilesPersistence:
    """
    Class to handle the persistence of configuration files.
    """

    def __init__(self):
        self._program_version = 'Beta-1.1.2'
        self._ruta_documents_catalogo = self.get_ruta_documents()
        self._ruta_config = self.get_ruta_config_file()


    #region SETTERS AND GETTERS
    @property
    def ruta_documents_catalogo(self):
        """
        Get the path to the 'catalogo' folder in 'Documents'.
        :return: Path to the 'catalogo' folder.
        """
        return self._ruta_documents_catalogo


    @ruta_documents_catalogo.setter
    def ruta_documents_catalogo(self, value):
        """
        Set the path to the 'catalogo' folder in 'Documents'.
        :param value: Path to the 'catalogo' folder.
        """
        self._ruta_documents_catalogo = value


    @property
    def ruta_config(self):
        """
        Get the path to the configuration file.
        :return: Path to the configuration file.
        """
        return self._ruta_config


    @ruta_config.setter
    def ruta_config(self, value):
        """
        Set the path to the configuration file.
        :param value: Path to the configuration file.
        """
        self._ruta_config = value

    @property
    def program_version(self):
        """
        Get the program version.
        :return: Program version.
        """
        return self._program_version
#endregion


    @staticmethod
    def get_ruta_documents():
        """
        Get the path to the 'Documents' folder and create a 'catalogo' folder if it doesn't exist.
        :return:
        """
        documentos = os.path.join(os.path.expanduser('~'), 'Documents')
        ruta_carpeta = os.path.join(documentos, 'catalogo')
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

        return ruta_carpeta

    @staticmethod
    def encontrar_ruta_icono():
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # En el caso de PyInstaller
            base_path = sys._MEIPASS
        else:
            # En el caso de ejecutar directamente el script
            base_path = os.path.abspath(".")

        # Construir la ruta al archivo de icono
        icon_path = os.path.join(base_path, "Resources/program_icon.png")
        return icon_path


    def get_ruta_config_file(self):
        """
        Get the path to the configuration file within the 'catalogo' folder.
        :return:
        """
        return os.path.join(self._ruta_documents_catalogo, 'config.txt')


    def get_ruta_bdd(self):
        with open(self._ruta_config, 'rt') as config_file:
            lines = config_file.readlines()
            new_ruta_bdd = lines[1].replace('\n', '')
            return new_ruta_bdd


    def set_new_bbd_route_in_config(self, ruta_new: str):
        with open(self._ruta_config, 'rt') as config_file:
            config_lines = config_file.readlines()

        config_lines[1] = ruta_new

        with open(self._ruta_config, 'wt') as config_file:
            config_file.writelines(config_lines)


    def is_first_time_running(self):
        try:
            with open(self.ruta_config, 'rt') as archivo_config:
                return False
        except FileNotFoundError:
            with open(self.ruta_config, 'wt') as archivo_config:
                contenido_lineas = "journal\n"
                archivo_config.write(contenido_lineas * 2)
                return True


    def obtener_tema(self):
        config_file = open(self.ruta_config, 'rt')
        config_lines = config_file.readlines()
        config_file.close()
        tema = config_lines[0].replace('\n', '')
        return tema


    def cambiar_tema_config(self, new_tema):
        config_file = open(self._ruta_config, 'rt')
        config_lines = config_file.readlines()
        config_file.close()

        config_lines[0] = f'{new_tema}\n'

        config_file = open(self._ruta_config, 'wt')
        config_file.writelines(config_lines)
        config_file.close()