import ttkbootstrap as ttk
from Views.base_window_toplevel import BaseProjectWindowToplevel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Controllers.find_product_controller import FindProductController

# Beta 0.1.1


class VentanaBuscar(BaseProjectWindowToplevel):

    def __init__(self, parent, controller: 'FindProductController'):
        super().__init__(parent)
        self.controller = controller

        # ----------------------------------------- ventana ---------------------------------------------
        #resolution = project_functions.calcular_res_ventana() TODO CHECK CHECK CHECK
        parent.withdraw()
        self.title(f'{parent.title()} - Busqueda de productos')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.maximizar()
        # -----------------------------------------------frames---------------------------------------------------

        # Esta clase no implementa frames propios

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # --------------------------- buttons --------------------------

        # Esta clase no implementa botones propios

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=self.frame, textvariable=self.str_buscado, width=105)

        # --------------------------- labels ---------------------------
        self.label_titulo = ttk.Label(master=self.frame, text='Búsqueda de productos', font='Calibri 24 bold')

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)
        self.cuadro.bind("<Return>", self.registrar_venta)
        self.cuadro.bind("<Double-1>", self.registrar_venta)
        self.str_buscado.trace_add('write', self.realizar_busqueda) # TODO CHECK THIS
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        self.frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.label_titulo.pack_configure(pady=10)
        self.entry.pack_configure(pady=10, fill='x', expand=True)
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.pack_configure(fill='both', expand=True)
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')


    # ----------------------------------------- Métodos de esta clase ---------------------------------------------

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        self.controller.search_products(self.str_buscado.get())


    def registrar_venta(self, _event):
        valores = self.get_info_from_selected_item()
        product_id = valores[4]
        #VentanaVenta(self, product_id)
        self.controller.open_sale_register_window(product_id)

    def get_info_from_selected_item(self):
        tuple_item = self.cuadro.selection()
        item = tuple_item[0]
        if item:
            valores = self.cuadro.item(item, option='values')
            return valores
        return None
