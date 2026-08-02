import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import SearchTable, IHasTable, MixinTableNavigation
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView


from app.infrastructure.ui.tkinter.controllers.actions.show_product_controller import ShowProductController

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.models.producto import Producto


class ShowProductsView(BaseProjectView, IHasTable, MixinTableNavigation):

    def __init__(self, master):
        super().__init__(master)
        # inicializar el mixin
        MixinTableNavigation.__init__(self)
        self.controller = ShowProductController(self)
        # -----------------------------------------------frames---------------------------------------------------

        # Esta clase no implementa frames propios

        # -----------------------------------------ttk_variables------------------------------------------------
        self.lost_focus = ttk.BooleanVar()

        # -----------------------------------------Custom Widgets------------------------------------------------

        self._table = SearchTable(self, self.resolution_str, self.resolution, 'Búsqueda de productos')

        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<Configure>", self.table.adjust_size)
        self.bind("<Escape>", self.volver_al_menu)
        self.parent.bind("<Down>", self.change_focus_down)
        self.parent.bind("<Up>", self._on_up_press)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.controller.finished_init()

    @property
    def table(self) -> 'SearchTable':
        return self._table

    def pasar_al_cuadro(self, product_list: list['Producto']):
        self.table.show_products(product_list)


    def entry_action(self, *args):
        self.realizar_busqueda()


    def alphabetical_search_action(self):
        self.realizar_busqueda()


    def search_action(self):
        self.realizar_busqueda()


    def table_action(self, event):
        self.registrar_venta(event)


    def render_view(self):
        super().render_base()
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')
        self.table.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.table.render()


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        self.controller.search_products(self.table.get_search())


    def registrar_venta(self, _event):
        valores = self.get_info_from_selected_item()
        if not valores:
            return
        product_id = valores[4]
        self.controller.open_sale_register_window(product_id)


    def get_info_from_selected_item(self):
        tuple_item = self.table.get_selected()
        if not tuple_item:
            return None
        item = tuple_item[0]
        if item:
            valores = self.table.get_item_data(item)
            return valores
        return None

    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self.parent.bind("<Down>", self.clear_event)
        self.parent.bind("<Up>", self.clear_event)
        super().volver_al_menu(_varname=_varname,_index=_index,_mode=_mode)
