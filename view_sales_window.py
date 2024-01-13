import ttkbootstrap as ttk
import project_functions

# alpha 0.0.10


class VentanaVerVentas(ttk.Toplevel):
    # ----------------------------------------- Métodos de esta clase ---------------------------------------------
    def realizar_busqueda_sale(self):
        a = project_functions.busqueda_venta_fecha(self.fecha_var)
        if a:
            project_functions.pasar_al_cuadro_ventas(a, self.cuadro)
        else:
            self.cuadro.delete(*self.cuadro.get_children())

    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 2 / 5), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 5), anchor="center")
        self.cuadro.column("col3", width=int(new_width / 5), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 5), anchor="center")

    # ---------------------------------- ventana Principal de la clase ----------------------------------------
    def __init__(self, parent):
        super().__init__()
        resolution = project_functions.calcular_res_ventana()
        parent.withdraw()
        self.parent = parent
        # ----------------------------------------- ventana ---------------------------------------------
        self.title(f'{parent.title()} - Listado de ventas')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.geometry(resolution[0])
        self.state('zoomed')
        # -----------------------------------------------frames---------------------------------------------------
        self.frame = ttk.Frame(master=self)
        self.sub_frame = ttk.Frame(master=self.frame)

        # -----------------------------------------ttk variables------------------------------------------------
        self.fecha_var = ttk.StringVar()

        # -----------------------------------------bootstrap widgets------------------------------------------------
        # --------------------------- buttons --------------------------
        self.menu_button = ttk.Button(master=self, text='Volver al menú',
                                      command=lambda: project_functions.volver_al_menu(self, self.parent))

        self.button_theme = ttk.Button(master=self, textvariable=parent.str_modo,
                                       command=lambda: project_functions.cambiar_modo(
                                           project_functions.obtener_config('tema'), self.parent, parent.str_modo))

        # --------------------------- entry's --------------------------

        self.calendario = ttk.DateEntry(master=self)
        self.calendario.entry.configure(textvariable=self.fecha_var)

        # --------------------------- labels ---------------------------
        # none

        # --------------------------- cuadro ---------------------------
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        self.cuadro = ttk.Treeview(master=self.sub_frame, columns=("col1", "col2", "col3", "col4"))
        self.cuadro.column("#0")
        self.cuadro.column("col1")
        self.cuadro.column("col2")
        self.cuadro.column("col3")
        self.cuadro.column("col4")

        self.cuadro.heading("#0", text="Producto", anchor='center')
        self.cuadro.heading("col1", text="Cantidad", anchor='center')
        self.cuadro.heading("col2", text="Precio_total", anchor='center')
        self.cuadro.heading("col3", text="Fecha", anchor='center')
        self.cuadro.heading("col4", text="Hora", anchor='center')

        self.screen_width = int(resolution[1] * 1.3)
        self.screen_width = int(self.screen_width * 0.9)

        self.cuadro.column("#0", width=int(self.screen_width * 2 / 5), anchor="center")
        self.cuadro.column("col1", width=int(self.screen_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(self.screen_width / 5), anchor="center")
        self.cuadro.column("col3", width=int(self.screen_width / 5), anchor="center")
        self.cuadro.column("col4", width=int(self.screen_width / 5), anchor="center")

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
        self.scrollbar = ttk.Scrollbar(self.sub_frame, orient="vertical", command=self.cuadro.yview)
        self.scrollbar.pack(side="right", fill="y")

        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.fecha_var.trace_add("write", lambda *Args: self.realizar_busqueda_sale())
        self.bind("<Configure>", self.on_resize)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.menu_button.place(x=15, y=15, anchor='nw')
        self.frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.5, anchor="center")
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.pack_configure(fill='both', expand=True)
        self.button_theme.place(relx=0.990, rely=0.017, anchor='ne')
        self.calendario.place(relx=0.5, y=60, anchor='center')
