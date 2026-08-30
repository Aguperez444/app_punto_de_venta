from __future__ import annotations

import calendar
from datetime import datetime, timedelta
from tkinter import filedialog
from typing import TYPE_CHECKING
import ttkbootstrap as ttk

from app.application.dto.sales_dto import SaleSummaryDTO
from app.infrastructure.ui.tkinter.controllers.actions.show_sales_controller import (
    ShowSalesController,
)
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView

if TYPE_CHECKING:
    from app.domain.models.venta import Venta


def shift_date_by_days(base_date: datetime, days: int) -> datetime:
    """Desplaza una fecha la cantidad indicada de días (positiva o negativa)."""
    return base_date + timedelta(days=days)


def shift_date_by_months(base_date: datetime, months: int) -> datetime:
    """Desplaza una fecha por meses ajustando el día al último día válido del mes destino."""
    month_index = (base_date.month - 1) + months
    target_year = base_date.year + (month_index // 12)
    target_month = (month_index % 12) + 1
    last_day = calendar.monthrange(target_year, target_month)[1]
    target_day = min(base_date.day, last_day)
    return base_date.replace(year=target_year, month=target_month, day=target_day)


class ShowSalesListView(BaseProjectView):
    _DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ShowSalesController(self)

        self.resolution = self.get_screen_resolution()
        self.resolution_str = f"{self.resolution[0]}x{self.resolution[1]}"
        self.frame_para_total = ttk.Frame(master=self)
        self.actions_frame = ttk.Frame(master=self)
        self.date_nav_frame = ttk.Frame(master=self)

        self._current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        self.fecha_var = ttk.StringVar(value=self._current_date.strftime(self._DATE_FORMAT))
        self.total_price_of_day = ttk.StringVar(value="")
        self.mode_txt = ttk.StringVar(value="Ver listado por mes")
        self.mode = ttk.IntVar(value=1)
        self.title_mode = ttk.StringVar(value="Total del Día: ")
        self.prev_btn_txt = ttk.StringVar(value="◀ Día anterior")
        self.next_btn_txt = ttk.StringVar(value="Día siguiente ▶")

        self.button_mode = ttk.Button(
            master=self,
            textvariable=self.mode_txt,
            width=20,
            style="my.TButton",
            command=self.change_mode,
        )
        self.button_prev = ttk.Button(
            master=self.date_nav_frame,
            textvariable=self.prev_btn_txt,
            width=18,
            bootstyle="info",
            command=self.go_previous_period,
        )
        self.button_next = ttk.Button(
            master=self.date_nav_frame,
            textvariable=self.next_btn_txt,
            width=18,
            bootstyle="info",
            command=self.go_next_period,
        )

        self.button_detail = ttk.Button(
            master=self.actions_frame,
            text="Ver detalle de venta",
            width=20,
            bootstyle="info",
            command=self.open_selected_sale_detail,
        )
        self.button_export = ttk.Button(
            master=self.actions_frame,
            text="Exportar a CSV",
            width=18,
            bootstyle="success-outline",
            command=self.export_sales_csv,
        )

        self.calendario = ttk.DateEntry(
            self.date_nav_frame,
            dateformat=self._DATE_FORMAT,
            startdate=self._current_date.date(),
        )
        self.calendario.entry.configure(textvariable=self.fecha_var)
        self.fecha_var.set(self._current_date.strftime(self._DATE_FORMAT))

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

        self.cuadro.tag_configure(
            "par", foreground="black", background="white", font=("Calibri", font_size)
        )
        self.cuadro.tag_configure(
            "impar", foreground="white", background="grey", font=("Calibri", font_size)
        )

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
        self.parent.bind("<Left>", self._on_left_arrow)
        self.parent.bind("<Right>", self._on_right_arrow)
        self.bind("<Destroy>", self._cleanup_bindings)
        self.es_primer_resize = True

        self.controller.finished_init()
        self.realizar_busqueda_sale()
        self.cuadro.focus_set()

    def _apply_column_widths(self, total_width: int) -> None:
        self.cuadro.column("#0", width=int(total_width * 2 / 5), anchor="center")
        self.cuadro.column("col1", width=int(total_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(total_width / 5), anchor="center")
        self.cuadro.column("col3", width=int(total_width / 5), anchor="center")
        self.cuadro.column("col4", width=int(total_width / 5), anchor="center")

    def render_view(self):
        self.menu_button.place(x=15, y=14, anchor="nw")
        self.button_theme.place(relx=0.990, y=14, anchor="ne")
        self.button_mode.place(y=14, relx=0.5, anchor="n")

        self.button_prev.grid(row=0, column=0, padx=(0, 10))
        self.calendario.grid(row=0, column=1, padx=4)
        self.button_next.grid(row=0, column=2, padx=(10, 0))
        self.date_nav_frame.place(relx=0.5, y=72, anchor="center")

        self.frame.place(relx=0.5, rely=0.45, relwidth=0.9, relheight=0.52, anchor="center")
        self.cuadro.pack_configure(fill="both", expand=True)
        self.sub_frame.pack_configure(fill="both", expand=True)

        self.button_detail.grid(row=0, column=0, padx=8)
        self.button_export.grid(row=0, column=1, padx=8)
        self.actions_frame.place(relx=0.5, rely=0.78, anchor="center")

        self.titulo_total_dia.grid(row=0, column=0)
        self.total_del_dia.grid(row=0, column=1)
        self.frame_para_total.place(relx=0.5, rely=0.88, anchor="center")

    def _parse_current_date(self) -> datetime | None:
        fecha_del_dia = self.fecha_var.get().strip()
        if not fecha_del_dia:
            return None
        for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
            try:
                parsed = datetime.strptime(fecha_del_dia, fmt)
                self._current_date = parsed
                return parsed
            except ValueError:
                continue
        return None

    def realizar_busqueda_sale(self, _varname=None, _index=None, _mode=None):
        fecha_obj = self._parse_current_date()
        if fecha_obj is None:
            return

        if self.mode.get() == 1:
            self.controller.get_ventas_del_dia(fecha_obj)
        else:
            self.controller.get_ventas_del_mes(fecha_obj)

    def _step_period(self, delta: int) -> None:
        base = self._parse_current_date() or self._current_date
        if self.mode.get() == 1:
            target = shift_date_by_days(base, delta)
        else:
            target = shift_date_by_months(base, delta)
        self._current_date = target
        self.fecha_var.set(target.strftime(self._DATE_FORMAT))

    def go_previous_period(self) -> None:
        self._step_period(-1)

    def go_next_period(self) -> None:
        self._step_period(1)

    def _is_main_window_active(self) -> bool:
        if not self.winfo_exists():
            return False
        focused = self.parent.focus_get()
        if focused is not None and focused.winfo_toplevel() != self.parent:
            return False
        if focused == self.calendario.entry:
            return False
        return True

    def _on_left_arrow(self, _event=None):
        if self._is_main_window_active():
            self.go_previous_period()
            return "break"
        return None

    def _on_right_arrow(self, _event=None):
        if self._is_main_window_active():
            self.go_next_period()
            return "break"
        return None

    def _cleanup_bindings(self, event=None):
        if event is not None and event.widget is not self:
            return
        try:
            self.parent.unbind("<Left>")
            self.parent.unbind("<Right>")
        except Exception:
            pass

    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self._cleanup_bindings()
        super().volver_al_menu(_varname=_varname, _index=_index, _mode=_mode)

    def export_sales_csv(self):
        output_path = filedialog.asksaveasfilename(
            title="Exportar listado de ventas a CSV",
            defaultextension=".csv",
            initialfile="ventas.csv",
            filetypes=[("Archivo CSV", "*.csv")],
        )
        if output_path:
            self.controller.export_current_sales_to_csv(output_path)

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
            self.prev_btn_txt.set("◀ Mes anterior")
            self.next_btn_txt.set("Mes siguiente ▶")
        else:
            self.mode.set(1)
            self.title_mode.set("Total del Día: ")
            self.mode_txt.set("Ver listado por mes")
            self.prev_btn_txt.set("◀ Día anterior")
            self.next_btn_txt.set("Día siguiente ▶")
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
