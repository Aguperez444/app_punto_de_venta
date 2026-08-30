from __future__ import annotations

from typing import TYPE_CHECKING
import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import IHasTable, SearchTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import (
    BaseProjectPopupWindow,
)

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_price_controller import (
        IndividualEditPriceController,
    )


class IndividualEditPricePopup(BaseProjectPopupWindow, IHasTable):
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

    def __init__(self, parent, controller: "IndividualEditPriceController"):
        super().__init__(parent, width=1080, height=620)
        self.controller = controller

        self.title("Actualizar precio manualmente")
        self.minsize(960, 560)
        self.center_on_parent(1080, 620)
        self.focus_set()

        self.porcentajes = [
            "0,1", "0,2", "0,5", "1", "1,2", "1,5", "1,9", "2", "2,2", "2,4", "2,5",
            "3", "5", "7", "10", "15", "20", "25", "50", "75", "100", "-50", "Personalizado",
        ]
        self.porcentaje_var = ttk.StringVar(value="1")
        self.custom_porcentaje_var = ttk.StringVar(value="")
        self.precio_var = ttk.StringVar(value="$")

        # Barra superior para aumento por porcentaje (sin superponerse con el título)
        self.top_bar = ttk.Frame(master=self, padding=(16, 12, 16, 4))
        self.increment_frame = ttk.Frame(master=self.top_bar)

        self.button_increment = ttk.Button(
            master=self.increment_frame,
            text=f"Aplicar %{self.porcentaje_var.get()} a el/los productos seleccionados",
            bootstyle="warning",
            command=self.actualizar_percent,
        )
        self.porcentaje_combobox = ttk.Combobox(
            master=self.increment_frame,
            textvariable=self.porcentaje_var,
            values=self.porcentajes,
            width=12,
            state="readonly",
        )
        self.porcentaje_combobox.set(self.porcentajes[3])
        self.custom_percent_entry = ttk.Entry(
            master=self.increment_frame,
            textvariable=self.custom_porcentaje_var,
            width=8,
        )

        # Cabecera e input manual
        self.label_alerta = ttk.Label(
            master=self,
            text="Aumentar precio manualmente",
            font="Arial 19 bold",
            wraplength=700,
        )
        self.sub_label_alerta = ttk.Label(
            master=self,
            text="Esto solo va a afectar a los productos seleccionados",
            font="arial 13 italic",
        )

        self.input_frame = ttk.Frame(master=self)
        self.label_input = ttk.Label(
            master=self.input_frame, text="Ingrese el nuevo precio:", font="Arial 12 bold"
        )
        self.entry = ttk.Entry(master=self.input_frame, textvariable=self.precio_var, width=22)

        self.buttons_frame = ttk.Frame(master=self)
        self.button_cancel = ttk.Button(
            master=self.buttons_frame,
            text="Cancelar",
            bootstyle="danger",
            width=18,
            command=self.cancelar,
        )
        self.button_confirm = ttk.Button(
            master=self.buttons_frame,
            text="Actualizar precio",
            bootstyle="success",
            width=18,
            command=self.aceptar,
        )

        self._table = SearchTable(
            self,
            self.resolution_str,
            self.resolution,
            "Productos seleccionados para el cambio:",
            "arial 14 italic",
        )

        self.porcentaje_var.trace_add("write", self.actualizar_valor)
        self.custom_porcentaje_var.trace_add("write", self.actualizar_valor)

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        self.aceptar()

    def aceptar(self):
        nuevo_precio_str = self.precio_var.get()
        self.controller.update_price_to_new(nuevo_precio_str)

    def cancelar(self):
        self.controller.cancelar_cambios()

    def get_effective_percentage_str(self) -> str:
        if self.porcentaje_var.get() == "Personalizado":
            return self.custom_porcentaje_var.get().strip().replace(",", ".")
        return self.porcentaje_var.get().strip().replace(",", ".")

    def actualizar_valor(self, _varname=None, _index=None, _mode=None):
        if self.porcentaje_var.get() == "Personalizado":
            self.custom_percent_entry.grid(row=0, column=2, padx=(6, 0))
            self.custom_percent_entry.focus_set()
        else:
            self.custom_percent_entry.grid_forget()
        pct = self.get_effective_percentage_str() or "..."
        self.button_increment.config(text=f"Aplicar %{pct} a el/los productos seleccionados")

    def actualizar_percent(self):
        porcentaje_str = self.get_effective_percentage_str()
        self.controller.update_price_by_percentage(porcentaje_str)

    def render_view(self):
        self.button_increment.grid(row=0, column=0, padx=(0, 6))
        self.porcentaje_combobox.grid(row=0, column=1)
        self.increment_frame.pack(side="right")
        self.top_bar.pack(fill="x")

        self.label_alerta.pack(pady=(6, 2))
        self.sub_label_alerta.pack(pady=(0, 12))

        self.label_input.grid(row=0, column=0, padx=(0, 8))
        self.entry.grid(row=0, column=1)
        self.input_frame.pack(pady=6)

        self.button_cancel.grid(row=0, column=0, padx=12)
        self.button_confirm.grid(row=0, column=1, padx=12)
        self.buttons_frame.pack(pady=(10, 14))

        self.table.pack(fill="both", expand=True, padx=24, pady=(0, 18))
        self.table.render_only_table()

        self.entry.focus_set()
        self.realizar_busqueda()

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        self.controller.get_products()
