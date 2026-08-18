from __future__ import annotations

from typing import TYPE_CHECKING
import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.controllers.actions.show_product_controller import (
    ShowProductController,
)
from app.infrastructure.ui.tkinter.custom_widgets.search_table import (
    IHasTable,
    MixinTableNavigation,
    SearchTable,
)
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView

if TYPE_CHECKING:
    from app.domain.models.producto import Producto


class ShowProductsView(BaseProjectView, IHasTable, MixinTableNavigation):
    def __init__(self, master):
        super().__init__(master)
        MixinTableNavigation.__init__(self)
        self.controller = ShowProductController(self)

        self.lost_focus = ttk.BooleanVar()
        self.cart_summary_var = ttk.StringVar(
            value="Carrito vacío — Enter en un producto registra venta rápida"
        )

        self._table = SearchTable(self, self.resolution_str, self.resolution, "Búsqueda de productos")

        self.cart_bar_frame = ttk.Frame(master=self, padding=(12, 8))
        self.label_cart_summary = ttk.Label(
            master=self.cart_bar_frame,
            textvariable=self.cart_summary_var,
            font="Arial 12 bold",
        )
        self.button_checkout_cart = ttk.Button(
            master=self.cart_bar_frame,
            text="Ver / Finalizar carrito (F2)",
            style="success",
            width=26,
            state="disabled",
            command=self.controller.open_cart_checkout,
        )
        self.button_clear_cart = ttk.Button(
            master=self.cart_bar_frame,
            text="Vaciar carrito",
            style="danger-outline",
            width=15,
            state="disabled",
            command=self.controller.clear_cart,
        )

        self.bind("<Configure>", self.table.adjust_size)
        self.bind("<Escape>", self.volver_al_menu)
        self.parent.bind("<Down>", self.change_focus_down)
        self.parent.bind("<Up>", self._on_up_press)
        self.parent.bind("<F2>", self._on_f2_checkout)
        self._table.entry.bind("<Return>", self._on_entry_return)

        self.controller.finished_init()

    @property
    def table(self) -> "SearchTable":
        return self._table

    def pasar_al_cuadro(self, product_list: list["Producto"]):
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
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor="ne")
        self.table.place(relx=0.5, rely=0.41, relwidth=0.9, relheight=0.62, anchor="center")
        self.table.render()

        self.label_cart_summary.pack(side="left", padx=(4, 16))
        self.button_clear_cart.pack(side="right", padx=6)
        self.button_checkout_cart.pack(side="right", padx=6)
        self.cart_bar_frame.place(relx=0.5, rely=0.83, relwidth=0.9, anchor="center")

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        term = self.table.get_search()
        if self.table.its_alphabetic_checked():
            self.controller.search_products_alphabetically(term)
        else:
            self.controller.search_products(term)

    def _on_entry_return(self, _event=None):
        term = self.table.get_search().strip()
        if not term:
            return
        if self.controller.try_open_by_exact_barcode(term):
            return
        self.table.grab_focus_cuadro()

    def _on_f2_checkout(self, _event=None):
        if self.controller.cart.has_items:
            self.controller.open_cart_checkout()

    def update_cart_summary(self, items_count: int, total_units: int, total_str: str):
        if items_count == 0:
            self.cart_summary_var.set("Carrito vacío — Enter en un producto registra venta rápida")
            self.button_checkout_cart.configure(state="disabled")
            self.button_clear_cart.configure(state="disabled")
        else:
            self.cart_summary_var.set(
                f"Carrito: {items_count} producto(s) ({total_units} u.) | Total: {total_str} — Enter añade al carrito"
            )
            self.button_checkout_cart.configure(state="normal")
            self.button_clear_cart.configure(state="normal")

    def focus_search_after_cart_add(self):
        self.table.str_buscado.set("")
        self.table.grab_focus()

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
            return self.table.get_item_data(item)
        return None

    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self.parent.bind("<Down>", self.clear_event)
        self.parent.bind("<Up>", self.clear_event)
        self.parent.bind("<F2>", self.clear_event)
        super().volver_al_menu(_varname=_varname, _index=_index, _mode=_mode)
