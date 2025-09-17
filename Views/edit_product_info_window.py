import ttkbootstrap as ttk

from Views.base_window_toplevel import BaseProjectWindowToplevel

from Controllers.individual_edit_info_controller import IndividualEditInfoController

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.edit_product_info_controller import EditProductInfoController


class VentanaEditInfo(BaseProjectWindowToplevel):

    def __init__(self, parent, controller: 'EditProductInfoController'):
        super().__init__(parent)

        self.controller = controller

        # ----------------------------------------- ventana ---------------------------------------------
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Editar info productos')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.attributes('-zoomed', True)

        # -----------------------------------------------frames---------------------------------------------------

        # Esta clase no implementa frames propios

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()
        self.order_mode = ttk.IntVar()
        # -----------------------------------------simple_variables------------------------------------------------

        # Esta clase no implementa variables simples

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # Esta clase no implementa widgets bootstrap propios

        # --------------------------- buttons --------------------------

        #esta clase no implementa botones propios

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=self.frame, textvariable=self.str_buscado, width=105)

        # --------------------------- labels ---------------------------
        self.label_titulo = ttk.Label(master=self.frame, text='Editar productos', font='Calibri 24 bold')


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

        self.controller.get_all_products()


    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.cuadro.selection()
        for item in tuple_items:
            valores = self.cuadro.item(item, option='values')
            mod_ids.append(valores[4]) # genera una lista con los ids de los productos seleccionados

        if len(mod_ids) > 1:
            self.show_error("Solo se puede editar un producto a la vez")
        elif len(mod_ids) == 0:
            self.show_error("No hay ningún producto seleccionado")
        else:
            id_producto = mod_ids[0]
            IndividualEditInfoController(self, id_producto)


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        filtro_busqueda = self.str_buscado.get()

        if filtro_busqueda == '':
            self.controller.get_all_products()
        elif self.alfabetico_checked.get() == 1:
            self.controller.get_filtered_products_alphabetically(filtro_busqueda)
        else:
            self.controller.get_filtered_products(filtro_busqueda)



