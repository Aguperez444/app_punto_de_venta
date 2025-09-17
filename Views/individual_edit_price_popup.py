import ttkbootstrap as ttk
from Views.base_window_toplevel import BaseProjectWindowToplevel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.individual_edit_price_controller import IndividualEditPriceController

class IndividualEditPricesPopup(BaseProjectWindowToplevel):

    def __init__(self, parent, controller: 'IndividualEditPriceController'):

        super().__init__(parent)

        self.controller = controller
        self.ancho = int(parent.winfo_width() / 1.2)
        self.alto = int(parent.winfo_height() / 1.2)
        self.x = (parent.winfo_screenwidth() - self.ancho) // 2
        self.y = (parent.winfo_screenheight() - self.alto) // 2

        self.title('Actualizar precio manualmente')
        self.geometry = f'{self.ancho}x{self.alto}+{self.x}+{self.y}'
        # alert_window.iconbitmap(parent.parent.icon_path)
        self.focus_set()

        self.porcentaje_var = ttk.StringVar(value='10')
        self.precio_var = ttk.StringVar(value='$')


        self.input_frame = ttk.Frame(master=self)
        self.increment_frame = ttk.Frame(master=self)
        self.buttons_frame = ttk.Frame(master=self)

        self.entry = ttk.Entry(master=self.input_frame, textvariable=self.precio_var)

        self.label_input = ttk.Label(master=self.input_frame, text='Ingrese el nuevo precio:', font='Arial 12 bold')
        self.label_alerta = ttk.Label(master=self, text='Aumentar precio manualmente',
                                      font='Arial 20 bold', wraplength=550)
        self.sub_label_alerta = ttk.Label(master=self, text='Esto solo va a afectar a los productos seleccionados',
                                          font='arial 15 italic')
        self.sub_label_2 = ttk.Label(master=self, text='Productos seleccionados para el cambio:',
                                     font='arial 15 italic')
        self.button_confirm = ttk.Button(master=self.buttons_frame, text='Actualizar precio', style='success')
        self.button_confirm.configure(width=15, command=self.aceptar)
        self.button_cancel = ttk.Button(master=self.buttons_frame, text='Cancelar', style='danger')
        self.button_cancel.configure(width=15, command=self.cancelar)
        self.button_increment = ttk.Button(master=self.increment_frame,
                                           text=f'Incrementar un %{self.porcentaje_var.get()} a el/los '
                                                f'productos seleccionados',
                                           style='warning', command=self.actualizar_percent)

        self.porcentajes = ['5', '10', '15', '20', '25', '50', '75', '100', '-50']
        self.porcentaje_combobox = ttk.Combobox(master=self.increment_frame, textvariable=self.porcentaje_var,
                                                values=self.porcentajes)
        self.porcentaje_combobox.configure(width=3, state='readonly')
        self.porcentaje_combobox.set(self.porcentajes[1])

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)
        self.porcentaje_var.trace_add("write", self.actualizar_valor)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        self.relleno_superior = ttk.Frame(self, height=44, width=0)


    def aceptar(self):
        nuevo_precio_str = self.precio_var.get()
        self.controller.update_price_to_new(nuevo_precio_str)


    def cancelar(self):
        self.controller.cancelar_cambios()

    def actualizar_valor(self, _varname=None, _index=None, _mode=None):
        self.button_increment.config(text=f"Incrementar un %{self.porcentaje_var.get()} a el/los productos seleccionados")

    def actualizar_percent(self):
        porcentaje_str = self.porcentaje_var.get()
        self.controller.update_price_by_percentage(porcentaje_str)

    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")



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
        self.button_increment.grid(row=0, column=0)
        self.porcentaje_combobox.grid(row=0, column=1)
        self.increment_frame.place(relx=0.99, rely=0.017, anchor='ne')
        self.sub_label_2.pack()
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.place(relx=0.5, rely=0.75, relwidth=0.8, relheight=0.4, anchor='center')

        self.controller.get_products()