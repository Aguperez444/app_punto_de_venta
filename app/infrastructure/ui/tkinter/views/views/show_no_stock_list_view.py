import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import IHasTable, SearchTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView


from app.infrastructure.ui.tkinter.controllers.actions.show_no_stock_controller import ShowNoStockController

class ShowNoStockView(BaseProjectView, IHasTable):


    def __init__(self, parent):
        super().__init__(parent)

        self.controller = ShowNoStockController(self)

        # -----------------------------------------------frames---------------------------------------------------

        self.increment_frame = ttk.Frame(master=self)

        # -----------------------------------------Custom widgets------------------------------------------------

        self._table = SearchTable(self, self.resolution_str, self.resolution, "Listado de productos fuera de stock")

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.table.adjust_size)
        self.controller.finished_init()


    @property
    def table(self) -> 'SearchTable':
        return self._table


    def table_action(self, event):
        self.edit_selected(event)


    def entry_action(self, *args):
        self.toggle_alphabetical_search()


    def search_action(self):
        self.realizar_busqueda()


    def alphabetical_search_action(self):
        self.realizar_busqueda_alfabetica()


    def render_view(self):
        # ---------------------------------------------- placing widgets -----------------------------------------------
        super().render_base()
        self.table.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.table.render()

        self.increment_frame.place(relx=0.82, rely=0.017, anchor='ne')

        self.controller.get_all_products_no_stock()


    def toggle_alphabetical_search(self):
        if self.table.its_alphabetic_checked():
            self.realizar_busqueda_alfabetica()
        else:
            self.realizar_busqueda()


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        filtro_busqueda = self.table.get_search()

        if filtro_busqueda == '':
            self.controller.get_all_products_no_stock()
        else:
            self.controller.get_filtered_products_no_stock(filtro_busqueda)


    def realizar_busqueda_alfabetica(self):
        filtro_busqueda = self.table.get_search()

        if filtro_busqueda == '':
            self.controller.get_all_products_no_stock_alphabetically()
        else:
            self.controller.get_filtered_products_no_stock_alphabetically(filtro_busqueda)

    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.table.get_selected()
        for item in tuple_items:
            valores = self.table.get_item_data(item)
            mod_ids.append(int(valores[4])) # El ID está en la columna oculta (col4), esta línea añade todos los ID seleccionados a una lista

        self.controller.open_edit_stock_controller_window(mod_ids)

