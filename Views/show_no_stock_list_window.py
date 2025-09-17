import ttkbootstrap as ttk
from Views.base_window_abstract_class import BaseProjectWindowToplevel
from Controllers.individual_edit_stock_controller import IndividualEditStockController

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.show_no_stock_controller import ShowNoStockController

class VentanaNoStock(BaseProjectWindowToplevel):

    def __init__(self, parent, controller: 'ShowNoStockController'):
        super().__init__(parent)

        self.controller = controller

        # ----------------------------------------- ventana ---------------------------------------------
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Añadir stock')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())

        self.maximizar()

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
        self.increment_frame.place(relx=0.82, rely=0.017, anchor='ne')

        # se ejecuta instantáneamente
        self.controller.get_all_products_no_stock()


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        filtro_busqueda = self.str_buscado.get()

        if filtro_busqueda == '':
            self.controller.get_all_products_no_stock()
        elif self.alfabetico_checked.get() == 1:
            self.controller.get_filtered_products_no_stock_alphabetically(filtro_busqueda)
        else:
            self.controller.get_filtered_products_no_stock(filtro_busqueda)


    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.cuadro.selection()
        for item in tuple_items:
            valores = self.cuadro.item(item, option='values') # Obtiene los valores de las filas seleccionadas
            mod_ids.append(valores[4]) # El ID está en la columna oculta (col4), esta línea añade todos los ID seleccionados a una lista

        IndividualEditStockController(self, mod_ids) # abre la ventana de edición individual
