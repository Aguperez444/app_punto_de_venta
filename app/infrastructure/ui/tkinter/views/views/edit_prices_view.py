import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import IHasTable, SearchTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView


from app.infrastructure.ui.tkinter.controllers.actions.edit_prices_controller import EditPricesController


class EditPricesView(BaseProjectView, IHasTable):


    def __init__(self, parent):
        super().__init__(parent)
        self.actual_focus = 0
        self.controller = EditPricesController(self)
        # ----------------------------------------- ventana ---------------------------------------------

        # -----------------------------------------------frames---------------------------------------------------
        self.increment_frame = ttk.Frame(master=self)

        # -----------------------------------------ttk_variables------------------------------------------------
        self.porcentaje_var = ttk.StringVar(value='1')
        # -----------------------------------------simple_variables------------------------------------------------
        self.porcentajes = ['0,1', '0,2', '0,5', '1', '1,2', '1,5', '1,9', '2', '2,2', '2,4', '2,5', '3', '5', '7', '10', '15', '20', '25', '50', '75', '100', '-50', 'Personalizado']
        # TODO, AÑADIR LÓGICA PARA PORCENTAJES PERSONALIZADOS

        # ------------------------------------------ Custom Widgets ------------------------------------------------

        self._table = SearchTable(self, self.resolution_str, self.resolution, "Actualización de precios")

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # --------------------------- buttons --------------------------

        self.button_increment = ttk.Button(master=self.increment_frame, text=f'Incrementar un %{self.porcentaje_var.get()} '
                                                                             'a todos los precios', style='warning',
                                           command=self.increment_all)
        # --------------------------- entry's --------------------------
        self.porcentaje_combobox = ttk.Combobox(master=self.increment_frame, textvariable=self.porcentaje_var,
                                                values=self.porcentajes)
        self.porcentaje_combobox.set(self.porcentajes[3]) # poner por default en 1%
        self.porcentaje_combobox.configure(width=3, state='readonly')




        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.table.adjust_size)
        self.porcentaje_var.trace_add("write", self.actualizar_valor)

        self.controller.finished_init()


    @property
    def table(self) -> SearchTable:
        return self._table


    def table_action(self, event):
        self.edit_selected(event)


    def entry_action(self, *args):
        self.toggle_alphabetic_search()

    def search_action(self):
        self.realizar_busqueda()


    def alphabetical_search_action(self):
        self.realizar_busqueda_alfabetica()

    def render_view(self):
        # ---------------------------------------------- placing widgets -----------------------------------------------
        super().render_base()

        self.table.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.table.render()

        self.button_increment.grid(row=0, column=0, ipady=3)
        self.porcentaje_combobox.grid(row=0, column=1, ipady=3)
        self.increment_frame.place(relx=0.82, rely=0.017, anchor='ne')


        self.controller.get_all_products()


    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.table.get_selected()
        for item in tuple_items:
            valores = self.table.get_item_data(item)
            mod_ids.append(int(valores[4]))

        self.controller.open_individual_edit_price_window(mod_ids)


    def actualizar_valor(self, *_args):
        self.button_increment.config(text=f'Incrementar un %{self.porcentaje_var.get()} a todos los precios')


    def toggle_alphabetic_search(self):
        if self.table.its_alphabetic_checked():
            self.realizar_busqueda_alfabetica()
        else:
            self.realizar_busqueda()


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        filtro_busqueda = self.table.get_search()

        if filtro_busqueda == '' or filtro_busqueda == ' ':
            self.controller.get_all_products()
        else:
            self.controller.get_filtered_products(filtro_busqueda)


    def realizar_busqueda_alfabetica(self):
        filtro_busqueda = self.table.get_search()

        if filtro_busqueda == '' or filtro_busqueda == ' ':
            self.controller.get_all_products_alphabetically()
        else:
            self.controller.get_filtered_products_alphabetically(filtro_busqueda)

    def increment_all(self):
        self.controller.open_update_all_prices_window()


    def confirmar_cambios(self):
        porcentaje_elegido = self.porcentaje_var.get()
        porcentaje_elegido = porcentaje_elegido.replace(',', '.')
        self.controller.update_all_prices(porcentaje_elegido)


    def cambios_realizados(self, percentage):
        self.show_message(f"Se han incrementado correctamente los precios en un %{percentage}")
        self.realizar_busqueda()