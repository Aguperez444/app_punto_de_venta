from __future__ import annotations

from typing import TYPE_CHECKING
import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import (
    BaseProjectPopupWindow,
)

if TYPE_CHECKING:
    from app.application.services.sale_cart import SaleCart
    from app.infrastructure.ui.tkinter.controllers.actions.show_product_controller import (
        ShowProductController,
    )


class CartCheckoutPopup(BaseProjectPopupWindow):
    """Popup de revisión y confirmación del carrito multi-producto."""

    def __init__(self, parent, controller: "ShowProductController", cart: "SaleCart"):
        super().__init__(parent, width=960, height=540)
        self.controller = controller
        self.cart = cart
        self.title("Carrito de Venta")
        self.minsize(840, 480)
        self.center_on_parent(960, 540)
        self.focus_set()

        self.header_frame = ttk.Frame(master=self)
        self.table_frame = ttk.Frame(master=self)
        self.item_controls_frame = ttk.Frame(master=self)
        self.footer_frame = ttk.Frame(master=self)

        self.label_title = ttk.Label(
            master=self.header_frame,
            text="Carrito de Venta",
            font="Arial 18 bold",
        )
        self.label_hint = ttk.Label(
            master=self.header_frame,
            text="Revise los productos, ajuste cantidades o presione Enter para confirmar la venta.",
            font="Arial 10 italic",
        )

        self.tree = ttk.Treeview(
            master=self.table_frame,
            columns=("codigo", "cantidad", "precio_unitario", "subtotal"),
            show="tree headings",
        )
        self.tree.heading("#0", text="Producto", anchor="center")
        self.tree.heading("codigo", text="Código", anchor="center")
        self.tree.heading("cantidad", text="Cantidad", anchor="center")
        self.tree.heading("precio_unitario", text="Precio unit.", anchor="center")
        self.tree.heading("subtotal", text="Subtotal", anchor="center")

        self.tree.column("#0", width=310, minwidth=180, anchor="w", stretch=True)
        self.tree.column("codigo", width=115, minwidth=80, anchor="center", stretch=True)
        self.tree.column("cantidad", width=95, minwidth=70, anchor="center", stretch=True)
        self.tree.column("precio_unitario", width=140, minwidth=115, anchor="e", stretch=True)
        self.tree.column("subtotal", width=145, minwidth=115, anchor="e", stretch=True)

        self.tree.tag_configure("par", foreground="black", background="white", font=("Calibri", 12))
        self.tree.tag_configure("impar", foreground="white", background="grey", font=("Calibri", 12))
        self.tree.bind("<Configure>", self._on_tree_resize)

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.btn_plus = ttk.Button(
            master=self.item_controls_frame,
            text="+1 unidad",
            bootstyle="info-outline",
            width=12,
            command=lambda: self._adjust_selected(1),
        )
        self.btn_minus = ttk.Button(
            master=self.item_controls_frame,
            text="-1 unidad",
            bootstyle="info-outline",
            width=12,
            command=lambda: self._adjust_selected(-1),
        )
        self.btn_remove = ttk.Button(
            master=self.item_controls_frame,
            text="Quitar ítem",
            bootstyle="warning-outline",
            width=14,
            command=self._remove_selected,
        )
        self.btn_clear = ttk.Button(
            master=self.item_controls_frame,
            text="Vaciar carrito",
            bootstyle="danger-outline",
            width=14,
            command=self._clear_cart,
        )

        self.total_var = ttk.StringVar(value="")
        self.label_total = ttk.Label(
            master=self.footer_frame,
            textvariable=self.total_var,
            font="Arial 16 bold",
        )
        self.btn_continue = ttk.Button(
            master=self.footer_frame,
            text="Seguir agregando",
            bootstyle="secondary",
            width=18,
            command=self.destroy,
        )
        self.btn_confirm = ttk.Button(
            master=self.footer_frame,
            text="Confirmar venta (Enter)",
            bootstyle="success",
            width=22,
            command=self._confirm_sale,
        )

        self.render_view()

    def _on_tree_resize(self, event):
        usable = max(event.width - 20, 560)
        self.tree.column("#0", width=int(usable * 0.36))
        self.tree.column("codigo", width=int(usable * 0.14))
        self.tree.column("cantidad", width=int(usable * 0.12))
        self.tree.column("precio_unitario", width=int(usable * 0.19))
        self.tree.column("subtotal", width=int(usable * 0.19))

    def render_view(self):
        self.label_title.pack(pady=(12, 2))
        self.label_hint.pack(pady=(0, 8))
        self.header_frame.pack(fill="x", padx=20)

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=8)

        self.btn_plus.grid(row=0, column=0, padx=6)
        self.btn_minus.grid(row=0, column=1, padx=6)
        self.btn_remove.grid(row=0, column=2, padx=6)
        self.btn_clear.grid(row=0, column=3, padx=6)
        self.item_controls_frame.pack(pady=6)

        self.label_total.pack(side="left", padx=10)
        self.btn_confirm.pack(side="right", padx=6)
        self.btn_continue.pack(side="right", padx=6)
        self.footer_frame.pack(fill="x", padx=20, pady=(8, 16))

        self.refresh_table()

    def refresh_table(self):
        selected = self.tree.selection()
        selected_id = selected[0] if selected else None

        self.tree.delete(*self.tree.get_children())
        for idx, line in enumerate(self.cart.lines):
            tag = "par" if idx % 2 == 0 else "impar"
            pid = str(line.producto.id_producto)
            self.tree.insert(
                "",
                "end",
                iid=pid,
                text=line.producto.nombre,
                values=(
                    line.producto.codigo,
                    line.cantidad,
                    str(line.producto.precio),
                    str(line.subtotal_precio),
                ),
                tags=(tag,),
            )

        if selected_id and self.tree.exists(selected_id):
            self.tree.selection_set(selected_id)

        self.total_var.set(f"Total ({self.cart.total_units} u.): {self.cart.total}")
        self.btn_confirm.configure(state="normal" if self.cart.has_items else "disabled")

    def _get_selected_product_id(self) -> int | None:
        selection = self.tree.selection()
        if not selection:
            self.show_error("Seleccione un producto del carrito.")
            return None
        return int(selection[0])

    def _adjust_selected(self, delta: int):
        product_id = self._get_selected_product_id()
        if product_id is None:
            return
        for line in self.cart.lines:
            if line.producto.id_producto == product_id:
                self.cart.update_quantity(product_id, line.cantidad + delta)
                break
        self.controller.notify_cart_changed()
        self.refresh_table()

    def _remove_selected(self):
        product_id = self._get_selected_product_id()
        if product_id is None:
            return
        self.cart.remove_item(product_id)
        self.controller.notify_cart_changed()
        self.refresh_table()

    def _clear_cart(self):
        self.controller.clear_cart()
        self.refresh_table()

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        self._confirm_sale()

    def _confirm_sale(self):
        if self.cart.is_empty:
            self.show_error("El carrito está vacío.")
            return
        if self.controller.confirm_cart_sale(parent_popup=self):
            self.destroy()
