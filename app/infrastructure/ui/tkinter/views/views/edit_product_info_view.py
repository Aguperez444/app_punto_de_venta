from app.infrastructure.ui.tkinter.custom_widgets.search_table import SearchTable, IHasTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView

from app.infrastructure.ui.tkinter.controllers.actions.edit_product_info_controller import EditProductInfoController


class EditProductInfoView(BaseProjectView, IHasTable):

    def __init__(self, parent):
        super().__init__(parent)

        self.controller = EditProductInfoController(self)

        # -----------------------------------------CustomWidgets------------------------------------------------

        self._table = SearchTable(self, self.resolution_str, self.resolution, 'Editar productos')

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.table.adjust_size)
        self.bind("<Escape>", self.volver_al_menu)

        self.controller.finished_init()


    @property
    def table(self) -> 'SearchTable':
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
        super().render_base()
        self.table.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.table.render()

        self.controller.get_all_products()


    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.table.get_selected()
        for item in tuple_items:
            valores = self.table.get_item_data(item)
            mod_ids.append(int(valores[4])) # genera una lista con los ids de los productos seleccionados

        if len(mod_ids) > 1:
            self.show_error("Solo se puede editar un producto a la vez")
        elif len(mod_ids) == 0:
            self.show_error("No hay ningún producto seleccionado")
        else:
            id_producto = mod_ids[0]
            self.controller.open_individual_edit_info_window(id_producto)


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        filtro_busqueda = self.table.get_search()

        if filtro_busqueda == '':
            self.controller.get_all_products()
        else:
            self.controller.get_filtered_products(filtro_busqueda)


    def realizar_busqueda_alfabetica(self):
        filtro_busqueda = self.table.get_search()

        if filtro_busqueda == '':
            self.controller.get_all_products_alphabetically()
        else:
            self.controller.get_filtered_products_alphabetically(filtro_busqueda)


    def toggle_alphabetic_search(self):
        if self.table.its_alphabetic_checked():
            self.realizar_busqueda_alfabetica()
        else:
            self.realizar_busqueda()



