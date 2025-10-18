from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView
from app.infrastructure.ui.tkinter.custom_widgets.search_table import SearchTable, IHasTable

from app.infrastructure.ui.tkinter.controllers.actions.add_stock_controller import AddStockController


class AddStockView(BaseProjectView, IHasTable):

    def __init__(self, master):
        super().__init__(master)
        self.controller = AddStockController(self)

        # -----------------------------------------------Custom Widgets-------------------------------------------------
        self._table = SearchTable(self, self.resolution_str, self.resolution, 'Añadir Stock')

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.table.adjust_size)
        self.bind("<Escape>", self.volver_al_menu)

        self.controller.finished_init()

    @property
    def table(self) -> SearchTable:
        return self._table


    def render_view(self):
        # ---------------------------------------------- placing widgets -----------------------------------------------
        super().render_base()
        self.table.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.table.render()

        self.obtener_datos_productos()


    def obtener_datos_productos(self):
        self.controller.get_all_products()


    def obtener_datos_filtrados(self, buscado: str):
        self.controller.get_filtered_products(buscado)

    def table_action(self, event):
        self.edit_selected(event)


    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.table.get_selected()
        for item in tuple_items:
            item_data = self.table.get_item_data(item) # Obtiene los valores de las filas seleccionadas
            mod_ids.append(int(item_data[4])) # El ID está en la columna oculta (col4), esta línea añade todos los ID seleccionados a una lista
        self.controller.open_individual_edit_window(mod_ids)


    def entry_action(self, *args):
        self.toggle_alphabetic_search()


    def search_action(self):
        self.realizar_busqueda()


    def alphabetical_search_action(self, *args):
        self.realizar_busqueda_alfabetica()


    def toggle_alphabetic_search(self):
        if self.table.its_alphabetic_checked():
            self.realizar_busqueda_alfabetica()
        else:
            self.realizar_busqueda()

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        buscado = self.table.get_search()
        if buscado == '':
            self.obtener_datos_productos()
        else:
            self.obtener_datos_filtrados(buscado)


    def realizar_busqueda_alfabetica(self):
        filtro_busqueda = self.table.get_search()

        if filtro_busqueda == '' or filtro_busqueda == ' ':
            self.controller.get_all_products_alphabetically()
        else:
            self.controller.get_filtered_products_alphabetically(filtro_busqueda)


    def pasar_al_cuadro(self, products):
        self.table.show_products(products)
