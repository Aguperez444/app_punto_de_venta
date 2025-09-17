import ttkbootstrap as ttk

from Controllers.individual_edit_price_controller import IndividualEditPriceController
from Controllers.update_all_prices_controller import UpdateAllPricesController

from Views.base_window_toplevel import BaseProjectWindowToplevel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.edit_prices_controller import EditPricesController


class VentanaPrecios(BaseProjectWindowToplevel):

    def __init__(self, parent, controller: 'EditPricesController'):
        super().__init__(parent)
        self.actual_focus = 0
        self.controller = controller
        # ----------------------------------------- ventana ---------------------------------------------
        self.parent.withdraw() # esconder la ventana padre
        self.title(f'{self.parent.title()} - Editar precios')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy()) # se encarga de cerrar la ventana padre al cerrarse esta
        self.maximizar()

        # -----------------------------------------------frames---------------------------------------------------
        self.increment_frame = ttk.Frame(master=self)

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()
        self.porcentaje_var = ttk.StringVar(value='1')
        # -----------------------------------------simple_variables------------------------------------------------
        self.porcentajes = ['0,1', '0,2', '0,5', '1', '1,2', '1,5', '1,9', '2', '2,2', '2,4', '2,5' '3', '5', '7', '10', '15', '20', '25', '50', '75', '100', '-50', 'Personalizado']

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # --------------------------- buttons --------------------------

        self.button_increment = ttk.Button(master=self.increment_frame, text=f'Incrementar un %{self.porcentaje_var.get()} '
                                                                             'a todos los precios', style='warning',
                                           command=self.increment_all)
        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=self.frame, textvariable=self.str_buscado, width=105)
        self.porcentaje_combobox = ttk.Combobox(master=self.increment_frame, textvariable=self.porcentaje_var,
                                                values=self.porcentajes)
        self.porcentaje_combobox.set(self.porcentajes[3]) # setear por default en 1%
        self.porcentaje_combobox.configure(width=3, state='readonly')

        # --------------------------- labels ---------------------------
        self.label_titulo = ttk.Label(master=self.frame, text='Actualización de precios', font='Calibri 24 bold')



        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)

        self.cuadro.bind("<Return>", self.edit_selected)
        self.cuadro.bind("<Double-1>", self.edit_selected)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        self.str_buscado.trace_add('write', self.realizar_busqueda)
        self.porcentaje_var.trace_add("write", self.actualizar_valor)

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
        self.button_increment.grid(row=0, column=0, ipady=3)
        self.porcentaje_combobox.grid(row=0, column=1, ipady=3)
        self.increment_frame.place(relx=0.82, rely=0.017, anchor='ne')


        self.controller.get_all_products()


    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.cuadro.selection()
        for item in tuple_items:
            valores = self.cuadro.item(item, option='values')
            mod_ids.append(valores[4])


        IndividualEditPriceController(self, mod_ids)


    def actualizar_valor(self, *_args):
        self.button_increment.config(text=f'Incrementar un %{self.porcentaje_var.get()} a todos los precios')


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        filtro_busqueda = self.str_buscado.get()

        if filtro_busqueda == '':
            self.controller.get_all_products()
        elif self.alfabetico_checked.get() == 1:
            self.controller.get_filtered_products_alphabetically(filtro_busqueda)
        else:
            self.controller.get_filtered_products(filtro_busqueda)


    def increment_all(self):
        UpdateAllPricesController(self)


    def confirmar_cambios(self):
        porcentaje_elegido = self.porcentaje_var.get()
        porcentaje_elegido = porcentaje_elegido.replace(',', '.')
        self.controller.update_all_prices(porcentaje_elegido)


    def cambios_realizados(self):
        self.realizar_busqueda()