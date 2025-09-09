#import project_functions
from Views.main_menu_window import MainWindowC
from Controllers.program_start_controller import ProgramStartController


# beta 0.1.0

# -------------------------------------------- Chequear_primer_arranque ------------------------------------------------
# ZOLD
#if project_functions.is_first_time_running():
#    project_functions.buscar_base_de_datos()

# NEW
program_start_controller = ProgramStartController()
program_start_controller.verify_first_run()
program_start_controller = None
# ---------------------------------------------------- App Mainloop ----------------------------------------------------

main_window1 = MainWindowC()
main_window1.mainloop()
