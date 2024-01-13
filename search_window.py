import ttkbootstrap as ttk
import project_functions
from sale_register_window import VentanaVenta

# alpha 0.0.10


class VentanaBuscar(ttk.Toplevel):
    # ----------------------------------------- Métodos de esta clase ---------------------------------------------
    def realizar_busqueda(self):
        a = project_functions.busqueda(self.str_buscado)
        if a:
            project_functions.pasar_al_cuadro(a, self.cuadro)
        else:
            self.cuadro.delete(*self.cuadro.get_children())

    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")

    def registrar_venta(self, event):
        tuple_items = self.cuadro.selection()
        item = tuple_items[0]
        if item and (event.keysym == 'Return' or event.num == 1):
            valores = self.cuadro.item(item, option='values')
            product_id = valores[4]
            VentanaVenta(self, product_id)

    # ---------------------------------- ventana Principal de la clase ----------------------------------------
    def __init__(self, parent):
        super().__init__()

        # ----------------------------------------- ventana ---------------------------------------------
        resolution = project_functions.calcular_res_ventana()
        parent.withdraw()
        self.parent = parent
        self.title(f'{parent.title()} - Busqueda de productos')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.geometry(resolution[0])
        self.state('zoomed')
        # -----------------------------------------------frames---------------------------------------------------
        frame = ttk.Frame(master=self)
        sub_frame = ttk.Frame(master=frame)

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # --------------------------- buttons --------------------------
        menu_button = ttk.Button(master=self, text='Volver al menú',
                                 command=lambda: project_functions.volver_al_menu(self, self.parent))

        button_theme = ttk.Button(master=self, textvariable=parent.str_modo,
                                  command=lambda: project_functions.cambiar_modo(
                                      project_functions.obtener_config('tema'), self.parent, parent.str_modo))
        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=frame, textvariable=self.str_buscado, width=105)

        # --------------------------- labels ---------------------------
        label_titulo = ttk.Label(master=frame, text='Busqueda de productos', font='Calibri 24 bold')

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
        self.cuadro.bind("<Return>", self.registrar_venta)
        self.cuadro.bind("<Double-1>", self.registrar_venta)
        self.str_buscado.trace_add('write', lambda *args: self.realizar_busqueda())
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        menu_button.place(x=15, y=15, anchor='nw')
        frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        label_titulo.pack_configure(pady=10)
        self.entry.pack_configure(pady=10, fill='x', expand=True)
        self.cuadro.pack_configure(fill='both', expand=True)
        sub_frame.pack_configure(fill='both', expand=True)
        button_theme.place(relx=0.990, rely=0.017, anchor='ne')
