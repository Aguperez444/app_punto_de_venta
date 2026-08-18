from __future__ import annotations

from typing import TYPE_CHECKING
import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import IHasTable, SearchTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import (
    BaseProjectPopupWindow,
)

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.controllers.individual_action.register_sale_controller import (
        RegisterSaleController,
    )


class SalesRegisterWindow(BaseProjectPopupWindow, IHasTable):
    @property
    def table(self) -> "SearchTable":
        return self._table

    def table_action(self, event):
        pass

    def entry_action(self, *args):
        pass

    def search_action(self):
        pass

    def alphabetical_search_action(self):
        pass

    def __init__(self, parent, controller: "RegisterSaleController", default_to_cart: bool = False):
        super().__init__(parent)
        self.controller = controller
        self.default_to_cart = default_to_cart

        self.tecla_presionada = False
        self._current_stock: int | None = None
        self.minsize(720, 480)
        self.focus_set()

        self.cantidad_vendida = ttk.StringVar(value="1")
        self.title_var = ttk.StringVar()
        self.stock_warning_var = ttk.StringVar(value="")

        self._table = SearchTable(
            self,
            self.resolution_str,
            self.resolution,
            "Producto seleccionado:",
            "Calibri 15 bold",
        )

        self.label_titulo = ttk.Label(master=self, text="", font="Calibri 18 bold", wraplength=660)
        self.entry_frame = ttk.Frame(master=self)
        self.label_entry = ttk.Label(master=self.entry_frame, text="Cantidad:", font="Calibri 14 bold")
        self.entry_cantidad_vendida = ttk.Entry(
            master=self.entry_frame, textvariable=self.cantidad_vendida, width=6
        )
        self.label_stock_warning = ttk.Label(
            master=self,
            textvariable=self.stock_warning_var,
            font="Calibri 10 italic",
            bootstyle="warning",
        )

        self.buttons_frame = ttk.Frame(master=self)

        # Cuando el carrito ya tiene productos, la opción default (Enter) pasa a ser "Añadir al carrito".
        # Cuando el carrito está vacío, la opción default (Enter) sigue siendo venta rápida directa.
        if self.default_to_cart:
            register_text = "Registrar venta directa"
            register_style = "primary-outline"
            cart_text = "Añadir al carrito (Enter)"
            cart_style = "success"
            hint_text = "Carrito activo: presione Enter para añadir al carrito."
        else:
            register_text = "Registrar venta (Enter)"
            register_style = "success"
            cart_text = "Añadir al carrito"
            cart_style = "info"
            hint_text = "Venta rápida: presione Enter para registrar venta directa o use 'Añadir al carrito'."

        self.cancel_button = ttk.Button(
            master=self.buttons_frame,
            text="Cancelar",
            style="danger",
            width=16,
            command=self.venta_cancel,
        )
        self.add_to_cart_button = ttk.Button(
            master=self.buttons_frame,
            text=cart_text,
            style=cart_style,
            width=22,
            command=self.add_to_cart,
        )
        self.confirm_button = ttk.Button(
            master=self.buttons_frame,
            text=register_text,
            style=register_style,
            width=22,
            command=self.venta_confirm,
        )
        self.label_hint = ttk.Label(master=self, text=hint_text, font="Calibri 10 italic")

        self.cantidad_vendida.trace_add("write", self._update_stock_warning)
        self.bind("<Configure>", self.table.adjust_size)
        self.bind("<KeyPress>", self.iniciar_actualizacion)
        self.bind("<KeyRelease>", self.detener_actualizacion)

    # region Funciones para manejo de UX
    def iniciar_actualizacion(self, event):
        if event.keysym not in ("Up", "Down"):
            return
        self.tecla_presionada = True
        self.actualizar_cantidad(event)

    def detener_actualizacion(self, _event):
        self.tecla_presionada = False

    def actualizar_cantidad(self, event):
        if self.tecla_presionada:
            raw = self.cantidad_vendida.get().strip()
            if raw.isdigit():
                val = int(raw)
                if event.keysym == "Up":
                    nueva_cantidad = val + 1
                elif event.keysym == "Down":
                    nueva_cantidad = max(1, val - 1)
                else:
                    return
                self.cantidad_vendida.set(str(nueva_cantidad))
                self.after(100, self.actualizar_cantidad, event)

    def _update_stock_warning(self, *_args):
        if self._current_stock is None:
            self.stock_warning_var.set("")
            return
        raw = self.cantidad_vendida.get().strip()
        if not raw.isdigit():
            self.stock_warning_var.set("")
            return
        qty = int(raw)
        resulting = self._current_stock - qty
        if resulting < 0:
            self.stock_warning_var.set(
                f"Aviso: el stock pasará a {resulting} (permitido para ventas sin stock cargado)."
            )
        else:
            self.stock_warning_var.set("")

    # endregion

    def render_view(self):
        self.label_titulo.pack(pady=(14, 6))

        self.label_entry.grid(row=0, column=0, padx=(0, 8))
        self.entry_cantidad_vendida.grid(row=0, column=1)
        self.entry_frame.pack(pady=(4, 2))
        self.label_stock_warning.pack(pady=(0, 6))

        self.table.pack(fill="x", padx=24, pady=6)
        self.table.render_only_table()

        self.cancel_button.grid(row=0, column=0, padx=8, ipady=10)
        self.add_to_cart_button.grid(row=0, column=1, padx=8, ipady=10)
        self.confirm_button.grid(row=0, column=2, padx=8, ipady=10)
        self.buttons_frame.pack(pady=(14, 4))
        self.label_hint.pack(pady=(0, 12))

        self.controller.show_product_data()
        self.entry_cantidad_vendida.focus_set()
        self.entry_cantidad_vendida.selection_range(0, "end")

    def adjust_product_text(self, product_name: str, current_stock: int | None = None):
        self._current_stock = current_stock
        if self.default_to_cart:
            self.title_var.set(f"Añadir al carrito o vender: {product_name}")
        else:
            self.title_var.set(f"¿Desea registrar una venta de: {product_name}?")
        self.label_titulo.configure(text=self.title_var.get())
        self._update_stock_warning()

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        if self.default_to_cart:
            self.add_to_cart()
        else:
            self.venta_confirm()

    def venta_confirm(self):
        amount_in = self.cantidad_vendida.get()
        self.controller.register_new_sale(amount_in)

    def add_to_cart(self):
        amount_in = self.cantidad_vendida.get()
        self.controller.add_to_cart(amount_in)

    def venta_cancel(self):
        self.destroy()
