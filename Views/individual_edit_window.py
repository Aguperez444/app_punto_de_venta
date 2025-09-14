import project_functions
import ttkbootstrap as ttk
from tkinter import messagebox
from Views.base_window_toplevel import BaseProjectWindowToplevel

class VentanaEditIndividual(BaseProjectWindowToplevel):

    def __init__(self, parent, controller):
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
        self.relleno_superior.pack(side=ttk.TOP)
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
        #self.sub_frame.place(relx=0.5, rely=0.75, relwidth=0.8, relheight=0.4, anchor='center')
        #self.frame.pack()
        self.frame.place(relx=0.5, rely=0.75, relwidth=0.8, relheight=0.4, anchor="center")
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.pack_configure(fill='both', expand=True)


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


    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")


class VentanaEditIndividual__OLD:

    def __init__(self, parent, mod_ids_in):
        self.parent = parent
        self.mod_ids_in = mod_ids_in
        self.ancho = int(parent.winfo_width() / 1.2)
        self.alto = int(parent.winfo_height() / 1.2)
        self.x = (parent.winfo_screenwidth() - self.ancho) // 2
        self.y = (parent.winfo_screenheight() - self.alto) // 2
        self.alert_window = ttk.Toplevel(parent)
        self.alert_window.title('Actualizar Stock de productos seleccionados')
        self.alert_window.geometry(f'{self.ancho}x{self.alto}+{self.x}+{self.y}')
        self.alert_window.focus_set()

        self.stock_var = ttk.StringVar(value='')

        self.productos = project_functions.busqueda_multiples_ids(mod_ids_in)

        self.input_frame = ttk.Frame(master=self.alert_window)
        self.increment_frame = ttk.Frame(master=self.alert_window)
        self.buttons_frame = ttk.Frame(master=self.alert_window)

        self.entry = ttk.Entry(master=self.input_frame, textvariable=self.stock_var)

        self.label_input = ttk.Label(master=self.input_frame, text='Ingrese el stock a agregar:', font='Arial 12 bold')
        self.label_alerta = ttk.Label(master=self.alert_window, text='Actualizar stock',
                                 font='Arial 20 bold', wraplength=550)
        self.sub_label_alerta = ttk.Label(master=self.alert_window, text='Esto solo va a afectar a los productos seleccionados',
                                     font='arial 15 italic')
        self.sub_label_2 = ttk.Label(master=self.alert_window, text='Productos seleccionados para el cambio:',
                                font='arial 15 italic')
        self.button_confirm = ttk.Button(master=self.buttons_frame, text='Añadir Stock', style='success')
        self.button_confirm.configure(width=15, command=self.aceptar)
        self.button_cancel = ttk.Button(master=self.buttons_frame, text='Cancelar', style='danger')
        self.button_cancel.configure(width=15, command=self.cancelar)

        self.frame_cuadro = ttk.Frame(master=self.alert_window, width=1000, height=400)

        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=30)
        self.cuadro = ttk.Treeview(master=self.frame_cuadro, columns=("col1", "col2", "col3", "col4"))
        self.cuadro.column("#0")
        self.cuadro.column("col1")
        self.cuadro.column("col2")
        self.cuadro.column("col3")
        self.cuadro.column("col4")

        self.cuadro.heading("#0", text="Producto", anchor='center')
        self.cuadro.heading("col1", text="Codigo", anchor='center')
        self.cuadro.heading("col2", text="Precio", anchor='center')
        self.cuadro.heading("col3", text="Detalle", anchor='center')
        self.cuadro.heading("col4", text="stock", anchor='center')

        self.cuadro.column("#0", width=int(self.ancho * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(self.ancho / 10), anchor="center")
        self.cuadro.column("col2", width=int(self.ancho / 10), anchor="center")
        self.cuadro.column("col3", width=int(self.ancho * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(self.ancho / 10), anchor="center")

        self.scrollbar = ttk.Scrollbar(self.frame_cuadro, orient="vertical", command=self.cuadro.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.style_scroll = ttk.Style()
        self.style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        project_functions.pasar_al_cuadro(self.productos, self.cuadro)

        self.alert_window.bind("<Configure>", self.on_resize)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        self.relleno_superior = ttk.Frame(self.alert_window, height=44, width=0)
        self.relleno_superior.pack(side=ttk.TOP)
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
        self.cuadro.pack_configure(fill='both', expand=True)
        self.frame_cuadro.place(relx=0.5, rely=0.75, relwidth=0.8, relheight=0.4, anchor='center')



    def aceptar(self):
        try:
            project_functions.add_to_stock(self.mod_ids_in, self.stock_var.get())
            self.alert_window.destroy()
            self.parent.realizar_busqueda()
        except SyntaxError:
            messagebox.showinfo('Error con la cantidad de stock', 'El la cantidad a agregar solo puede '
                                                                  'ser un numero entero positivo')

    def cancelar(self):
        self.alert_window.destroy()
        self.parent.realizar_busqueda()

    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")