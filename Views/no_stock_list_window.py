import ttkbootstrap as ttk
import project_functions
from Views.base_window_toplevel import BaseProjectWindowToplevel


# Beta 0.1.0

class VentanaNoStock(BaseProjectWindowToplevel):

    def __init__(self, parent):
        super().__init__(parent)
        # ----------------------------------------- ventana ---------------------------------------------
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Añadir stock')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())

        #self.state('zoomed') funciona en windows no en linux
        self.attributes('-zoomed', True)

        # -----------------------------------------------frames---------------------------------------------------

        self.increment_frame = ttk.Frame(master=self)

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()
        self.order_mode = ttk.IntVar()
        # -----------------------------------------simple_variables------------------------------------------------

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # --------------------------- buttons --------------------------

        # Esta clase no implementa botónes propios

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=self.frame, textvariable=self.str_buscado, width=105)

        # --------------------------- labels ---------------------------
        self.label_titulo = ttk.Label(master=self.frame, text='Listado de productos fuera de stock', font='Calibri 24 bold')


        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)
        self.str_buscado.trace_add('write', lambda *args: self.realizar_busqueda())
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        self.frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.label_titulo.pack_configure(pady=10)
        self.checkbutton.pack_configure(pady=10)
        self.entry.pack_configure(pady=10, fill='x', expand=True)
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.pack_configure(fill='both', expand=True)
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')
        self.increment_frame.place(relx=0.82, rely=0.017, anchor='ne')

        # se ejecuta instantáneamente
        self.pasar_al_cuadro(project_functions.get_no_stock())


    def realizar_busqueda(self):
        a = project_functions.busqueda_no_stock(self.str_buscado)
        if a:
            if self.order_mode.get() == 1:
                a.sort(key=lambda x: x[1])
            project_functions.pasar_al_cuadro(a, self.cuadro)
        else:
            self.cuadro.delete(*self.cuadro.get_children())
            if self.str_buscado.get() == '':
                a = project_functions.get_no_stock()
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

