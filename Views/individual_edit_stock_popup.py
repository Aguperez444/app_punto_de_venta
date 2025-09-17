import ttkbootstrap as ttk
from Views.base_window_toplevel import BaseProjectWindowToplevel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.individual_edit_stock_controller import IndividualEditStockController


class VentanaEditIndividual(BaseProjectWindowToplevel):

    def __init__(self, parent, controller: 'IndividualEditStockController'):
        super().__init__(parent)
        self.controller = controller
        self.title('Actualizar Stock de productos seleccionados')
        self.focus_set()


        self.stock_var = ttk.StringVar(value='')

        self.input_frame = ttk.Frame(master=self)
        self.increment_frame = ttk.Frame(master=self)
        self.buttons_frame = ttk.Frame(master=self)

        self.entry = ttk.Entry(master=self.input_frame, textvariable=self.stock_var)

        self.label_input = ttk.Label(master=self.input_frame, text='Ingrese el stock a agregar:', font='Arial 12 bold')
        self.label_alerta = ttk.Label(master=self, text='Actualizar stock',
                                 font='Arial 20 bold', wraplength=550)
        self.sub_label_alerta = ttk.Label(master=self, text='Esto solo va a afectar a los productos seleccionados',
                                     font='arial 15 italic')
        self.sub_label_2 = ttk.Label(master=self, text='Productos seleccionados para el cambio:',
                                font='arial 15 italic')
        self.button_confirm = ttk.Button(master=self.buttons_frame, text='Añadir Stock', style='success')
        self.button_confirm.configure(width=15, command=self.confirmar)
        self.button_cancel = ttk.Button(master=self.buttons_frame, text='Cancelar', style='danger')
        self.button_cancel.configure(width=15, command=self.cancelar)

        self.bind("<Configure>", self.on_resize)

        self.relleno_superior = ttk.Frame(self, height=44, width=0)


    def render_view(self):
        self.relleno_superior.pack(side='top')
        self.label_alerta.pack()
        self.sub_label_alerta.pack()
        self.button_cancel.grid(row=0, column=0, padx=15)
        self.button_confirm.grid(row=0, column=1, padx=15)
        self.label_input.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.input_frame.pack()
        self.buttons_frame.pack(pady=15)
        self.increment_frame.place(relx=0.99, rely=0.017, anchor='ne')
        self.sub_label_2.pack()
        self.frame.place(relx=0.5, rely=0.75, relwidth=0.8, relheight=0.4, anchor="center")
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.place(relx=0.5, rely=0.75, relwidth=0.8, relheight=0.4, anchor='center')


        self.controller.get_products_to_edit()


    def confirmar(self):
        quantity = int(self.stock_var.get())
        self.controller.confirmar_cambios(quantity)



    def cambios_realizados(self):
        self.destroy()
        self.parent.realizar_busqueda()


    def cancelar(self):
        self.destroy()
        self.parent.realizar_busqueda()
