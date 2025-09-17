import ttkbootstrap as ttk
from Views.base_window_abstract_class import BaseProjectWindowToplevel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.update_all_prices_controller import UpdateAllPricesController


class UpdateAllPricesPopup(BaseProjectWindowToplevel):

    def __init__(self, parent_window, controller: 'UpdateAllPricesController'):
        super().__init__(parent_window, needs_cuadro=False)
        self.controller = controller

        self.ancho = int(parent_window.winfo_width() / 1.2)
        self.alto = int(parent_window.winfo_height() / 2)
        self.x = (parent_window.winfo_screenwidth() - self.ancho) // 2
        self.y = (parent_window.winfo_screenheight() - self.alto) // 2

        self.title('Confirmar Actualización de precios')
        self.geometry = f'{self.ancho}x{self.alto}+{self.x}+{self.y}'

        self.focus_set()
        self.grab_set()

        self.buttons_frame = ttk.Frame(master=self)

        self.label_alerta = ttk.Label(master=self, text=(f'Esta seguro que desea incrementar los precios de todos los '
                                                            f'productos un %{parent_window.porcentaje_var.get()}'),
                                 font='Arial 20 bold', wraplength=550)
        self.sub_label_alerta = ttk.Label(master=self, text=('Esto va a afectar a TODOS los productos, no solo a los'
                                                                ' que aparecieron buscados por nombre'), wraplength=460)
        self.sub_label_alerta.configure(font='Arial 15 italic')
        self.button_confirm = ttk.Button(master=self.buttons_frame, text='Aceptar', style='warning')
        self.button_confirm.configure(width=15, command=self.aceptar)
        self.button_cancel = ttk.Button(master=self.buttons_frame, text='Cancelar', style='danger')
        self.button_cancel.configure(width=15, command=self.cancelar)


    def aceptar(self):
        self.controller.confirmar_cambios()


    def cancelar(self):
        self.controller.cancelar_cambios()


    def render_view(self):
        self.label_alerta.pack()
        self.sub_label_alerta.pack()
        self.button_cancel.grid(row=0, column=0, padx=15)
        self.button_confirm.grid(row=0, column=1, padx=15)
        self.buttons_frame.pack(pady=15)