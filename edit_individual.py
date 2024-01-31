import ttkbootstrap as ttk
import project_functions
from tkinter import messagebox


# Beta 0.1.0

class EditIndividual(ttk.Toplevel):

    def aceptar(self):
        try:
            project_functions.update_price_to_new(self.parent.mod_ids, self.precio_var.get())
            self.destroy()
            self.parent.realizar_busqueda()
        except SyntaxError:
            messagebox.showinfo('Error con el precio', 'El precio solo puede '
                                                       'ser un numero entero positivo')

    def cancelar(self):
        self.destroy()
        self.parent.realizar_busqueda()

    def actualizar_valor(self):
        self.button_increment.config(
            text=f"Incrementar un %{self.porcentaje_var.get()} a el/los productos seleccionados")

    def actualizar_percent(self):
        project_functions.update_selected(self.parent.mod_ids, self.porcentaje_var.get())
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

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        ancho = int(parent.winfo_width() / 1.2)
        alto = int(parent.winfo_height() / 1.2)
        x = (parent.winfo_screenwidth() - ancho) // 2
        y = (parent.winfo_screenheight() - alto) // 2
        self.title('Actualizar precio manualmente')
        self.geometry(f'{ancho}x{alto}+{x}+{y}')
        self.focus_set()
        self.iconbitmap('program_icon.ico')

        self.porcentaje_var = ttk.StringVar(value='10')
        self.precio_var = ttk.StringVar(value='$')

        productos = project_functions.busqueda_multiples_ids(parent.mod_ids)

        input_frame = ttk.Frame(master=self)
        increment_frame = ttk.Frame(master=self)
        buttons_frame = ttk.Frame(master=self)

        entry = ttk.Entry(master=input_frame, textvariable=self.precio_var)

        label_input = ttk.Label(master=input_frame, text='Ingrese el nuevo precio:', font='Arial 12 bold')
        label_alerta = ttk.Label(master=self, text='Aumentar precio manualmente',
                                 font='Arial 20 bold', wraplength=550)
        sub_label_alerta = ttk.Label(master=self, text='Esto solo va a afectar a los productos seleccionados',
                                     font='arial 15 italic')
        sub_label_2 = ttk.Label(master=self, text='Productos seleccionados para el cambio:',
                                font='arial 15 italic')
        button_confirm = ttk.Button(master=buttons_frame, text='Actualizar precio', style='success')
        button_confirm.configure(width=15, command=self.aceptar)
        button_cancel = ttk.Button(master=buttons_frame, text='Cancelar', style='danger')
        button_cancel.configure(width=15, command=self.aceptar)
        self.button_increment = ttk.Button(master=increment_frame, text=f'Incrementar un %{self.porcentaje_var.get()} a'
                                                                        f' el/los productos seleccionados',
                                           style='warning', command=self.actualizar_percent)

        porcentajes = ['5', '10', '15', '20', '25', '50', '75', '100', '-50']
        porcentaje_combobox = ttk.Combobox(master=increment_frame, textvariable=self.porcentaje_var, values=porcentajes)
        porcentaje_combobox.configure(width=3, state='readonly')
        porcentaje_combobox.set(porcentajes[1])

        frame_cuadro = ttk.Frame(master=self, width=1000, height=400)

        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        self.cuadro = ttk.Treeview(master=frame_cuadro, columns=("col1", "col2", "col3", "col4"))
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

        self.cuadro.column("#0", width=int(ancho * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(ancho / 10), anchor="center")
        self.cuadro.column("col2", width=int(ancho / 10), anchor="center")
        self.cuadro.column("col3", width=int(ancho * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(ancho / 10), anchor="center")

        scrollbar = ttk.Scrollbar(frame_cuadro, orient="vertical", command=self.cuadro.yview)
        scrollbar.pack(side="right", fill="y")

        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        project_functions.pasar_al_cuadro(productos, self.cuadro)

        self.bind("<Configure>", self.on_resize)
        self.porcentaje_var.trace_add("write", lambda *args: self.actualizar_valor())
        self.cuadro.configure(yscrollcommand=scrollbar.set)

        relleno_superior = ttk.Frame(self, height=44, width=0)
        relleno_superior.pack(side=ttk.TOP)
        label_alerta.pack()
        sub_label_alerta.pack()
        button_cancel.grid(row=0, column=0, padx=15)
        button_confirm.grid(row=0, column=1, padx=15)
        label_input.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        input_frame.pack()
        buttons_frame.pack(pady=15)
        self.button_increment.grid(row=0, column=0)
        porcentaje_combobox.grid(row=0, column=1)
        increment_frame.place(relx=0.99, rely=0.017, anchor='ne')
        sub_label_2.pack()
        self.cuadro.pack_configure(fill='both', expand=True)
        frame_cuadro.place(relx=0.5, rely=0.75, relwidth=0.8, relheight=0.4, anchor='center')
