from __future__ import annotations

import ttkbootstrap as ttk

from app.application.dto.sales_dto import SaleDetailDTO
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import (
    BaseProjectPopupWindow,
)


class SaleDetailPopup(BaseProjectPopupWindow):
    """Popup de solo lectura que muestra todos los ítems y subtotales de una venta."""

    def __init__(self, parent, sale_detail: SaleDetailDTO):
        super().__init__(parent)
        self.sale_detail = sale_detail
        self.title(f"Detalle de Venta #{sale_detail.venta_id or '-'}")
        self.minsize(720, 420)
        self.focus_set()

        self.header_frame = ttk.Frame(master=self)
        self.table_frame = ttk.Frame(master=self)
        self.footer_frame = ttk.Frame(master=self)

        self.label_title = ttk.Label(
            master=self.header_frame,
            text=f"Venta #{sale_detail.venta_id or '-'}",
            font="Arial 18 bold",
        )
        self.label_datetime = ttk.Label(
            master=self.header_frame,
            text=f"Fecha: {sale_detail.fecha_str}   |   Hora: {sale_detail.hora_str}",
            font="Arial 12",
        )

        self.tree = ttk.Treeview(
            master=self.table_frame,
            columns=("codigo", "cantidad", "precio_unitario", "subtotal"),
            show="tree headings",
        )
        self.tree.heading("#0", text="Producto", anchor="center")
        self.tree.heading("codigo", text="Código", anchor="center")
        self.tree.heading("cantidad", text="Cantidad", anchor="center")
        self.tree.heading("precio_unitario", text="Precio unitario", anchor="center")
        self.tree.heading("subtotal", text="Subtotal", anchor="center")

        self.tree.column("#0", width=260, anchor="w")
        self.tree.column("codigo", width=110, anchor="center")
        self.tree.column("cantidad", width=80, anchor="center")
        self.tree.column("precio_unitario", width=120, anchor="e")
        self.tree.column("subtotal", width=120, anchor="e")

        self.scrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.label_total = ttk.Label(
            master=self.footer_frame,
            text=f"Total de la venta: {sale_detail.total_str}",
            font="Arial 15 bold",
        )
        self.button_close = ttk.Button(
            master=self.footer_frame,
            text="Cerrar",
            style="secondary",
            width=16,
            command=self.destroy,
        )

        self.render_view()

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        self.destroy()

    def render_view(self):
        self.label_title.pack(pady=(12, 2))
        self.label_datetime.pack(pady=(0, 8))
        self.header_frame.pack(fill="x", padx=20)

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for idx, item in enumerate(self.sale_detail.items):
            tag = "par" if idx % 2 == 0 else "impar"
            self.tree.insert(
                "",
                "end",
                text=item.producto_nombre,
                values=(
                    item.producto_codigo,
                    item.cantidad,
                    item.precio_unitario_str,
                    item.subtotal_str,
                ),
                tags=(tag,),
            )

        self.label_total.pack(side="left", padx=10)
        self.button_close.pack(side="right", padx=10)
        self.footer_frame.pack(fill="x", padx=20, pady=(4, 16))
