import project_functions
from main import MainWindowC


# beta 0.1.0

# -------------------------------------------- Chequear_primer_arranque ------------------------------------------------
if project_functions.is_first_time_running():
    project_functions.buscar_base_de_datos()

# ---------------------------------------------------- App Mainloop ----------------------------------------------------
project_functions.set_ruta_bdd()

main_window1 = MainWindowC()

main_window1.mainloop()
