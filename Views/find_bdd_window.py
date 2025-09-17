import ttkbootstrap as ttk
from tkinter import filedialog, messagebox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.program_start_controller import ProgramStartController

class FindBddWindow(ttk.Window):
    def __init__(self, puntero_controller: 'ProgramStartController'):
        super().__init__()
        self.title('Seleccionar ruta de la base de datos')
        self.geometry('500x400')

        self.ruta_var = ttk.StringVar(value='')

        self.controller = puntero_controller
        self.button_explorer = ttk.Button(master=self, text='Buscar ruta', command=self.abrir_explorador)

        self.button_accept = ttk.Button(master=self, text='Confirmar', command=self.confirmar_ruta)

        self.etiqueta_ruta = ttk.Label(self, text='Ruta seleccionada: None')

        self.button_explorer.pack(pady=20)
        self.etiqueta_ruta.pack()
        self.button_accept.pack()


    def abrir_explorador(self):
        self.ruta_var.set(filedialog.askopenfilename())
        self.etiqueta_ruta.config(text=f'Ruta seleccionada: {self.ruta_var.get()}')


    def confirmar_ruta(self):
        if self.ruta_var.get() != '':
            self.controller.new_bdd_route_added(self.ruta_var.get())
            self.destroy()
        else:
            messagebox.showerror('Ruta incompleta', 'Porfavor ingrese una ruta valida')
