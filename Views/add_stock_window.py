import ttkbootstrap as ttk
import project_functions
from Views.base_window_toplevel import BaseProjectWindowToplevel
from Controllers.edit_individual_controller import EditIndividualController


# Beta 0.1.0


class VentanaStock(BaseProjectWindowToplevel):


    def __init__(self, parent, controller):
        super().__init__(parent)
        self.edit_individual_controller = None # will be used later to manage the edit individual window
        self.actual_focus = 0
        self.controller = controller
        # ----------------------------------------- ventana ---------------------------------------------
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Añadir stock')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        #self.state('zoomed') funciona en windows no en linux
        self.attributes('-zoomed', True)

        # -----------------------------------------------frames---------------------------------------------------

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()
        self.order_mode = ttk.IntVar()
        # -----------------------------------------simple_variables------------------------------------------------

        # esta clase no implementa variables simples, pero se deja el espacio para futuros cambios

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # --------------------------- buttons --------------------------

        # esta clase no implementa botónes adicionales, pero se deja el espacio para futuros cambios

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=self.frame, textvariable=self.str_buscado, width=105)

        # --------------------------- labels ---------------------------
        self.label_titulo = ttk.Label(master=self.frame, text='Añadir Stock', font='Calibri 24 bold')

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)
        self.cuadro.bind("<Return>", self.edit_selected)
        self.cuadro.bind("<Double-1>", self.edit_selected)
        self.str_buscado.trace_add('write', self.realizar_busqueda)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)


    def render_view(self):
        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        self.frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.label_titulo.pack_configure(pady=10)
        self.check.pack_configure(pady=10)
        self.entry.pack_configure(pady=10, fill='x', expand=True)
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.pack_configure(fill='both', expand=True)
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')

        self.obtener_datos_productos()

    def obtener_datos_productos(self):
        datos_productos = self.controller.get_all_products()
        self.pasar_al_cuadro(datos_productos)


    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.cuadro.selection()
        for item in tuple_items:
            valores = self.cuadro.item(item, option='values') # Obtiene los valores de las filas seleccionadas
            mod_ids.append(valores[4]) # El ID está en la columna oculta (col4), esta línea añade todos los ID seleccionados a una lista

        #abrir_ventana_edit_individual(self, mod_ids) #TODO CAMBIAR ESTO

        self.edit_individual_controller = EditIndividualController(self, mod_ids)

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):# TODO CAMBIAR ESTO
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

    def realizar_busqueda_alfabetica(self):
        self.controller.get_all_products_alphabetically()
