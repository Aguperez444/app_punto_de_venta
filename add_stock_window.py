import ttkbootstrap as ttk
import project_functions
from tkinter import messagebox


# Beta 0.1.0

def abrir_ventana_edit_individual(parent, mod_ids_in):
    def aceptar():
        try:
            project_functions.add_to_stock(mod_ids_in, stock_var.get())
            alert_window.destroy()
            parent.realizar_busqueda()
        except SyntaxError:
            messagebox.showinfo('Error con la cantidad de stock', 'El la cantidad a agregar solo puede '
                                                                  'ser un numero entero positivo')

    def cancelar():
        alert_window.destroy()
        parent.realizar_busqueda()

    def on_resize(event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        cuadro.column("col1", width=int(new_width / 10), anchor="center")
        cuadro.column("col2", width=int(new_width / 10), anchor="center")
        cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        cuadro.column("col4", width=int(new_width / 10), anchor="center")

    ancho = int(parent.winfo_width() / 1.2)
    alto = int(parent.winfo_height() / 1.2)
    x = (parent.winfo_screenwidth() - ancho) // 2
    y = (parent.winfo_screenheight() - alto) // 2
    alert_window = ttk.Toplevel(parent)
    alert_window.title('Actualizar Stock de productos seleccionados')
    alert_window.iconbitmap(parent.parent.icon_path)
    alert_window.geometry(f'{ancho}x{alto}+{x}+{y}')
    alert_window.focus_set()

    stock_var = ttk.StringVar(value='')

    productos = project_functions.busqueda_multiples_ids(mod_ids_in)

    input_frame = ttk.Frame(master=alert_window)
    increment_frame = ttk.Frame(master=alert_window)
    buttons_frame = ttk.Frame(master=alert_window)

    entry = ttk.Entry(master=input_frame, textvariable=stock_var)

    label_input = ttk.Label(master=input_frame, text='Ingrese el stock a agregar:', font='Arial 12 bold')
    label_alerta = ttk.Label(master=alert_window, text='Actualizar stock',
                             font='Arial 20 bold', wraplength=550)
    sub_label_alerta = ttk.Label(master=alert_window, text='Esto solo va a afectar a los productos seleccionados',
                                 font='arial 15 italic')
    sub_label_2 = ttk.Label(master=alert_window, text='Productos seleccionados para el cambio:',
                            font='arial 15 italic')
    button_confirm = ttk.Button(master=buttons_frame, text='Añadir Stock', style='success')
    button_confirm.configure(width=15, command=aceptar)
    button_cancel = ttk.Button(master=buttons_frame, text='Cancelar', style='danger')
    button_cancel.configure(width=15, command=cancelar)

    frame_cuadro = ttk.Frame(master=alert_window, width=1000, height=400)

    style = ttk.Style()
    style.configure('Treeview', rowheight=30)
    cuadro = ttk.Treeview(master=frame_cuadro, columns=("col1", "col2", "col3", "col4"))
    cuadro.column("#0")
    cuadro.column("col1")
    cuadro.column("col2")
    cuadro.column("col3")
    cuadro.column("col4")

    cuadro.heading("#0", text="Producto", anchor='center')
    cuadro.heading("col1", text="Codigo", anchor='center')
    cuadro.heading("col2", text="Precio", anchor='center')
    cuadro.heading("col3", text="Detalle", anchor='center')
    cuadro.heading("col4", text="stock", anchor='center')

    cuadro.column("#0", width=int(ancho * 3 / 10), anchor="center")
    cuadro.column("col1", width=int(ancho / 10), anchor="center")
    cuadro.column("col2", width=int(ancho / 10), anchor="center")
    cuadro.column("col3", width=int(ancho * 3 / 10), anchor="center")
    cuadro.column("col4", width=int(ancho / 10), anchor="center")

    scrollbar = ttk.Scrollbar(frame_cuadro, orient="vertical", command=cuadro.yview)
    scrollbar.pack(side="right", fill="y")

    style_scroll = ttk.Style()
    style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

    project_functions.pasar_al_cuadro(productos, cuadro)

    alert_window.bind("<Configure>", on_resize)
    cuadro.configure(yscrollcommand=scrollbar.set)

    relleno_superior = ttk.Frame(alert_window, height=44, width=0)
    relleno_superior.pack(side=ttk.TOP)
    label_alerta.pack()
    sub_label_alerta.pack()
    button_cancel.grid(row=0, column=0, padx=15)
    button_confirm.grid(row=0, column=1, padx=15)
    label_input.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    input_frame.pack()
    buttons_frame.pack(pady=15)
    increment_frame.place(relx=0.99, rely=0.017, anchor='ne')
    sub_label_2.pack()
    cuadro.pack_configure(fill='both', expand=True)
    frame_cuadro.place(relx=0.5, rely=0.75, relwidth=0.8, relheight=0.4, anchor='center')


class VentanaStock(ttk.Toplevel):

    def edit_selected(self, event):
        mod_ids = []
        tuple_items = self.cuadro.selection()
        for item in tuple_items:
            valores = self.cuadro.item(item, option='values')
            mod_ids.append(valores[4])
        abrir_ventana_edit_individual(self, mod_ids)

    def realizar_busqueda(self):
        a = project_functions.busqueda(self.str_buscado)
        if a:
            if self.order_mode.get() == 1:
                a.sort(key=lambda x: x[1])
            project_functions.pasar_al_cuadro(a, self.cuadro)
        else:
            self.cuadro.delete(*self.cuadro.get_children())
            if self.str_buscado.get() == '':
                a = project_functions.get_all()
                if self.order_mode.get() == 1:
                    a.sort(key=lambda x: x[1])
                project_functions.pasar_al_cuadro(a, self.cuadro)

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
        self.actual_focus = 0
        # ----------------------------------------- ventana ---------------------------------------------
        resolution = project_functions.calcular_res_ventana()
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Añadir stock')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.geometry(resolution[0])
        self.state('zoomed')
        self.iconbitmap(parent.icon_path)
        # -----------------------------------------------frames---------------------------------------------------
        frame = ttk.Frame(master=self)
        sub_frame = ttk.Frame(master=frame)
        increment_frame = ttk.Frame(master=self)

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()
        self.order_mode = ttk.IntVar()
        # -----------------------------------------simple_variables------------------------------------------------

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # --------------------------- buttons --------------------------
        menu_button = ttk.Button(master=self, text='Volver al menú',  width=17, style='my.TButton',
                                 command=lambda: project_functions.volver_al_menu(self, self.parent))

        button_theme = ttk.Button(master=self, textvariable=parent.str_modo,  width=17, style='my.TButton',
                                  command=lambda: project_functions.cambiar_modo(
                                      project_functions.obtener_config('tema'), self.parent, parent.str_modo))

        checkbutton = ttk.Checkbutton(master=frame, text="Mostrar en orden alfabético", variable=self.order_mode,
                                      command=self.realizar_busqueda)

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=frame, textvariable=self.str_buscado, width=105)

        # --------------------------- labels ---------------------------
        label_titulo = ttk.Label(master=frame, text='Añadir Stock', font='Calibri 24 bold')

        # --------------------------- cuadro ---------------------------
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        self.cuadro = ttk.Treeview(master=sub_frame, columns=("col1", "col2", "col3", "col4"))
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

        screen_width = int(resolution[1] * 1.3)
        screen_width = int(screen_width * 0.9)

        self.cuadro.column("#0", width=int(screen_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(screen_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(screen_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(screen_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(screen_width / 10), anchor="center")

        font_per_res = {'1476x830': 18,
                        '1353x761': 18,
                        '1292x807': 17,
                        '1230x692': 16,
                        '1107x692': 16,
                        '1050x590': 15,
                        '984x615': 14,
                        '984x787': 13,
                        '984x738': 13,
                        '984x553': 13,
                        '787x590': 12,
                        '615x461': 10}

        self.cuadro.tag_configure('par', foreground="black", background="white",
                                  font=('Calibri', font_per_res[resolution[0]],))
        self.cuadro.tag_configure('impar', foreground="white", background="grey",
                                  font=('Calibri', font_per_res[resolution[0]],))

        # ------------------------- scroll bar -------------------------
        self.scrollbar = ttk.Scrollbar(sub_frame, orient="vertical", command=self.cuadro.yview)
        self.scrollbar.pack(side="right", fill="y")

        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)
        self.cuadro.bind("<Return>", self.edit_selected)
        self.cuadro.bind("<Double-1>", self.edit_selected)
        self.str_buscado.trace_add('write', lambda *args: self.realizar_busqueda())
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        label_titulo.pack_configure(pady=10)
        checkbutton.pack_configure(pady=10)
        self.entry.pack_configure(pady=10, fill='x', expand=True)
        self.cuadro.pack_configure(fill='both', expand=True)
        sub_frame.pack_configure(fill='both', expand=True)
        button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')
        increment_frame.place(relx=0.82, rely=0.017, anchor='ne')

        # se ejecuta instantáneamente
        project_functions.pasar_al_cuadro(project_functions.get_all(), self.cuadro)
