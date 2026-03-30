from app.infrastructure.ui.tkinter.controllers.common.program_start_controller import ProgramStartController

# -------------------------------------------- Chequear_primer_arranque ------------------------------------------------

program_start_controller = ProgramStartController()
program_start_controller.verify_first_run()
program_start_controller = None
# ---------------------------------------------------- App Mainloop ----------------------------------------------------

from app.infrastructure.ui.tkinter.views.windows.main_menu_window import MainMenuWindow

main_window1 = MainMenuWindow()
main_window1.mainloop()
