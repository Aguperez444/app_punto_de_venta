import ttkbootstrap as ttk
from datetime import datetime
from Models.Venta import Venta
from Views.base_window_toplevel import BaseProjectWindowToplevel


# Beta 0.1.0


class VentanaVerVentas(BaseProjectWindowToplevel):
    # ---------------------------------- ventana Principal de la clase ----------------------------------------
    def __init__(self, parent, controller):
        super().__init__(parent, needs_cuadro=False)
        parent.withdraw()
        self.controller = controller
        # ----------------------------------------- ventana ---------------------------------------------
        self.title(f'{parent.title()} - Listado de ventas')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        #self.state('zoomed') funciona en windows no en linux
        self.attributes('-zoomed', True)
        self.resolution = self.get_screen_resolution()
        self.resolution_str = f'{self.resolution[0]}x{self.resolution[1]}'
        # -----------------------------------------------frames---------------------------------------------------
        self.frame_para_total = ttk.Frame(master=self)

        # -----------------------------------------ttk variables------------------------------------------------
        self.fecha_var = ttk.StringVar()
        self.total_price_of_day = ttk.StringVar(value='')
        self.mode_txt = ttk.StringVar(value='Ver listado por mes')
        self.mode = ttk.IntVar(value=1)
        self.title_mode = ttk.StringVar(value='Total del Día:')
        # -----------------------------------------bootstrap widgets------------------------------------------------
        # --------------------------- buttons --------------------------

        self.button_mode = ttk.Button(master=self, textvariable=self.mode_txt, width=17, style='my.TButton',
                                      command=self.change_mode)

        # --------------------------- entry's --------------------------

        self.calendario = ttk.DateEntry(master=self)
        self.calendario.entry.configure(textvariable=self.fecha_var)

        # --------------------------- labels ---------------------------
        self.total_del_dia = ttk.Label(master=self.frame_para_total, textvariable=self.total_price_of_day,
                                       font='Arial 15 bold')
        self.titulo_total_dia = ttk.Label(master=self.frame_para_total, textvariable=self.title_mode,
                                          font='Arial 15 bold')

        # el cuadro de esta ventana es distinto al resto, por esto se redefine
        # region --------------------------- cuadro ---------------------------
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

        self.screen_width = int(self.resolution[1] * 1.3)
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
                                  font=('Calibri', font_per_res[self.resolution_str],))
        self.cuadro.tag_configure('impar', foreground="white", background="grey",
                                  font=('Calibri', font_per_res[self.resolution_str],))

        # ------------------------- scroll bar -------------------------
        self.scrollbar = ttk.Scrollbar(self.sub_frame, orient="vertical", command=self.cuadro.yview)
        self.scrollbar.pack(side="right", fill="y")

        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        #endregion

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.fecha_var.trace_add("write", self.realizar_busqueda_sale) # TODO CHECK THIS
        self.bind("<Configure>", self.on_resize)

        # ---------------------------------------------- placing widgets -----------------------------------------------


    # ----------------------------------------- Métodos de esta clase ---------------------------------------------
    def render_view(self):
        self.menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        self.frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.5, anchor="center")
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.pack_configure(fill='both', expand=True)
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')
        self.button_mode.place(y=0.4, relx=0.5, anchor='n')
        self.calendario.place(relx=0.5, y=60, anchor='center')
        self.titulo_total_dia.grid(row=0, column=0)
        self.total_del_dia.grid(row=0, column=1)
        self.frame_para_total.place(relx=0.5, rely=0.87, anchor='center')


    def realizar_busqueda_sale(self, _varname=None, _index=None, _mode=None):

        fecha_del_dia = self.fecha_var.get()
        fecha_obj = datetime.strptime(fecha_del_dia, "%d/%m/%y").date()  # convertir string a date object

        if self.mode.get() == 1: # modo ventas del día
            self.controller.get_ventas_del_dia(fecha_obj)
        else: # modo ventas del mes
            self.controller.get_ventas_del_mes(fecha_obj)


    def on_resize(self, event):
        """
        Ajusta el tamaño de las columnas del treeview al redimensionar la ventana
        El ajuste para esta ventana es distinto al de las otras ventanas
        Por eso es necesario sobreescribir este method
        :param event:
        :return:
        """
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 2 / 5), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 5), anchor="center")
        self.cuadro.column("col3", width=int(new_width / 5), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 5), anchor="center")


    def change_mode(self):
        if self.mode.get() == 1:
            self.mode.set(2)
            self.mode_txt.set('Ver listado por día')
            self.title_mode.set('Total del Mes:')
        else:
            self.mode.set(1)
            self.title_mode.set('Total del Día:')
            self.mode_txt.set('Ver listado por mes')
        self.realizar_busqueda_sale()


    def pasar_al_cuadro_ventas(self, ventas_list: list[Venta]):
        self.cuadro.delete(*self.cuadro.get_children())
        contador = 0
        for venta in ventas_list:
            hora = venta.fecha.strftime('%H:%M:%S')
            fecha = venta.fecha.strftime('%d/%m/%Y')
            tag = 'par' if contador % 2 == 0 else 'impar'
            self.cuadro.insert("", "end", text=f'{venta.detalles[0].producto.producto}...',
                               values=(f'{venta.detalles[0].cantidad}...' , f'${round(venta.total_price, 2)}', fecha, hora), tags=tag)
            contador += 1


    def mostrar_total_ventas(self, total_ventas: str):
        self.total_price_of_day.set(total_ventas)

