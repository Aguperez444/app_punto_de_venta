from Views.find_bdd_window import FindBddWindow
from Database.config_files_persistance import ConfigFilesPersistence

class ProgramStartController:
    def __init__(self):

        self.config_persistance_pointer = ConfigFilesPersistence()
        self.boundary_pointer = None


    def find_bdd(self):
        self.boundary_pointer = FindBddWindow(self)
        self.boundary_pointer.mainloop()


    def verify_first_run(self):
        if self.config_persistance_pointer.is_first_time_running():
            self.find_bdd()


    def new_bdd_route_added(self, ruta):
        self.config_persistance_pointer.set_new_bbd_route_in_config(ruta)


