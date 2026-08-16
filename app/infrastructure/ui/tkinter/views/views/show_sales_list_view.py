from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
import ttkbootstrap as ttk

from app.application.dto.sales_dto import SaleSummaryDTO
from app.infrastructure.ui.tkinter.controllers.actions.show_sales_controller import (
    ShowSalesController,
)
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView

if TYPE_CHECKING:
    from app.domain.models.venta import Venta


class ShowSalesListView(BaseProjectView):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ShowSalesController(self)

        self.resolution = self.get_screen_resolution()
        self.resolution_str = f"{self.resolution[0]}x{self.resolution[1]}"
        self.frame_para_total = ttk.Frame(master=self)
        self.actions_frame = ttk.Frame(master=self)

        self.fecha_var = ttk.StringVar()
        self.total_price_of_day = ttk.StringVar(value="")
        self.mode_txt = ttk.StringVar(value="Ver listado por mes")
        self.mode = ttk.IntVar(value=1)
        self.title_mode = ttk.StringVar(value="Total del Día: ")

        self.button_mode = ttk.Button(
            master=self,
            textvariable=self.mode_txt,
            width=20,
            style="my.TButton",
            command=self.change_mode,
        )
        self.button_detail = ttk.Button(
            master=self.actions_frame,
            text="Ver detalle de venta",
            width=20,
            style="info",
            command=self.open_selected_sale_detail,
        )

        self.calendario = ttk.DateEntry(self)
        self.calendario.entry.configure(textvariable=self.fecha_var)

        self.total_del_dia = ttk.Label(
            master=self.frame_para_total,
            textvariable=self.total_price_of_day,
            font="Arial 15 bold",
        )
        self.titulo_total_dia = ttk.Label(
            master=self.frame_para_total,
            textvariable=self.title_mode,
            font="Arial 15 bold",
        )

        # region --------------------------- cuadro ---------------------------
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)
        self.cuadro = ttk.Treeview(master=self.sub_frame, columns=("col1", "col2", "col3", "col4"))
        self.cuadro.heading("#0", text="Producto(s)", anchor="center")
        self.cuadro.heading("col1", text="Unidades", anchor="center")
        self.cuadro.heading("col2", text="Precio total", anchor="center")
        self.cuadro.heading("col3", text="Fecha", anchor="center")
        self.cuadro.heading("col4", text="Hora", anchor="center")

        self.screen_width = int(int(self.resolution[1] * 1.3) * 0.9)
        self._apply_column_widths(self.screen_width)

        height = self.resolution[1] if self.resolution and len(self.resolution) > 1 else 600
        if height >= 800:
            font_size = 18
        elif height >= 690:
            font_size = 16
        elif height >= 590:
            font_size = 14
        elif height >= 500:
            font_size = 12
        else:
            font_size = 10

        self.cuadro.tag_configure("par", foreground="black", background="white", font=("Calibri", font_size))
        self.cuadro.tag_configure("impar", foreground="white", background="grey", font=("Calibri", font_size))

        self.scrollbar = ttk.Scrollbar(self.sub_frame, orient="vertical", command=self.cuadro.yview)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")
        # endregion

        self.fecha_var.trace_add("write", self.realizar_busqueda_sale)
        self.cuadro.bind("<Double-1>", self.open_selected_sale_detail)
        self.cuadro.bind("<Return>", self.open_selected_sale_detail)
        self.bind("<Configure>", self.on_resize)
        self.parent.bind("<Escape>", self.volver_al_menu)
        self.es_primer_resize = True

        self.controller.finished_init()

    def _apply_column_widths(self, total_width: int) -> None:
        self.cuadro.column("#0", width=int(total_width * 2 / 5), anchor="center")
        self.cuadro.column("col1", width=int(total_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(total_width / 5), anchor="center")
        self.cuadro.column("col3", width=int(total_width / 5), anchor="center")
        self.cuadro.column("col4", width=int(total_width / 5), anchor="center")

    def render_view(self):
        self.menu_button.place(x=15, rely=0.017, anchor="nw", height=35)
        self.frame.place(relx=0.5, rely=0.42, relwidth=0.9, relheight=0.52, anchor="center")
        self.cuadro.pack_configure(fill="both", expand=True)
        self.sub_frame.pack_configure(fill="both", expand=True)
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor="ne")
        self.button_mode.place(y=12, relx=0.5, anchor="n")
        self.calendario.place(relx=0.5, y=68, anchor="center")

        self.button_detail.grid(row=0, column=0, padx=8)
        self.actions_frame.place(relx=0.5, rely=0.76, anchor="center")

        self.titulo_total_dia.grid(row=0, column=0)
        self.total_del_dia.grid(row=0, column=1)
        self.frame_para_total.place(relx=0.5, rely=0.87, anchor="center")

    def realizar_busqueda_sale(self, _varname=None, _index=None, _mode=None):
        fecha_del_dia = self.fecha_var.get().strip()
        if not fecha_del_dia:
            return
        fecha_obj = None
        for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
            try:
                fecha_obj = datetime.strptime(fecha_del_dia, fmt)
                break
            except ValueError:
                continue
        if fecha_obj is None:
            return

        if self.mode.get() == 1:
            self.controller.get_ventas_del_dia(fecha_obj)
        else:
            self.controller.get_ventas_del_mes(fecha_obj)

    def open_selected_sale_detail(self, _event=None):
        selection = self.cuadro.selection()
        if not selection:
            self.show_error("Seleccione una venta para ver su detalle.")
            return
        try:
            venta_id = int(selection[0])
        except ValueError:
            return
        self.controller.open_sale_detail(venta_id)

    def on_resize(self, event):
        if self.es_primer_resize:
            self.es_primer_resize = False
            self.event_generate("<Configure>")
            return
        new_width = int(event.width * 0.9)
        self._apply_column_widths(new_width)

    def change_mode(self):
        if self.mode.get() == 1:
            self.mode.set(2)
            self.mode_txt.set("Ver listado por día")
            self.title_mode.set("Total del Mes: ")
        else:
            self.mode.set(1)
            self.title_mode.set("Total del Día: ")
            self.mode_txt.set("Ver listado por mes")
        self.realizar_busqueda_sale()

    def pasar_al_cuadro_ventas(self, ventas_list: list[SaleSummaryDTO | "Venta"]):
        self.cuadro.delete(*self.cuadro.get_children())
        for contador, item in enumerate(ventas_list):
            summary = item if isinstance(item, SaleSummaryDTO) else SaleSummaryDTO.from_domain(item)
            tag = "par" if contador % 2 == 0 else "impar"
            iid = str(summary.venta_id) if summary.venta_id is not None else f"row-{contador}"
            self.cuadro.insert(
                "",
                "end",
                iid=iid,
                text=summary.resumen_productos,
                values=(summary.cantidad_total, summary.total_str, summary.fecha_str, summary.hora_str),
                tags=(tag,),
            )

    def mostrar_total_ventas(self, total_ventas: str):
        self.total_price_of_day.set(total_ventas)
