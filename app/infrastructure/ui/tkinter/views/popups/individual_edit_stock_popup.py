from __future__ import annotations

from typing import TYPE_CHECKING
import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import IHasTable, SearchTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import (
    BaseProjectPopupWindow,
)

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_stock_controller import (
        IndividualEditStockController,
    )


class IndividualEditStockPopup(BaseProjectPopupWindow, IHasTable):
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

    def __init__(self, parent, controller: "IndividualEditStockController"):
        super().__init__(parent)
        self.controller = controller
        self.title("Actualizar Stock de productos seleccionados")
        self.focus_set()

        self.stock_var = ttk.StringVar(value="")
        self.mode_var = ttk.StringVar(value="add")

        self._table = SearchTable(
            self,
            self.resolution_str,
            self.resolution,
            "Productos seleccionados para el cambio:",
            "arial 15 italic",
        )

        self.mode_frame = ttk.Frame(master=self)
        self.input_frame = ttk.Frame(master=self)
        self.increment_frame = ttk.Frame(master=self)
        self.buttons_frame = ttk.Frame(master=self)

        self.radio_add = ttk.Radiobutton(
            master=self.mode_frame,
            text="Sumar stock",
            value="add",
            variable=self.mode_var,
            command=self._update_mode_labels,
        )
        self.radio_sub = ttk.Radiobutton(
            master=self.mode_frame,
            text="Restar stock",
            value="subtract",
            variable=self.mode_var,
            command=self._update_mode_labels,
        )
        self.radio_set = ttk.Radiobutton(
            master=self.mode_frame,
            text="Fijar stock exacto",
            value="set",
            variable=self.mode_var,
            command=self._update_mode_labels,
        )

        self.entry = ttk.Entry(master=self.input_frame, textvariable=self.stock_var)

        self.label_input = ttk.Label(
            master=self.input_frame, text="Ingrese el stock a sumar:", font="Arial 12 bold"
        )
        self.label_alerta = ttk.Label(
            master=self, text="Actualizar stock", font="Arial 20 bold", wraplength=550
        )
        self.sub_label_alerta = ttk.Label(
            master=self,
            text="Esto solo va a afectar a los productos seleccionados",
            font="arial 15 italic",
        )

        self.button_confirm = ttk.Button(
            master=self.buttons_frame, text="Sumar Stock", style="success", width=16, command=self.confirmar
        )
        self.button_cancel = ttk.Button(
            master=self.buttons_frame, text="Cancelar", style="danger", width=16, command=self.cancelar
        )

        self.bind("<Configure>", self.table.adjust_size)
        self.relleno_superior = ttk.Frame(self, height=24, width=0)

    def _update_mode_labels(self):
        mode = self.mode_var.get()
        if mode == "add":
            self.label_input.configure(text="Ingrese el stock a sumar:")
            self.button_confirm.configure(text="Sumar Stock", style="success")
        elif mode == "subtract":
            self.label_input.configure(text="Ingrese el stock a restar:")
            self.button_confirm.configure(text="Restar Stock", style="warning")
        else:
            self.label_input.configure(text="Ingrese el nuevo stock exacto:")
            self.button_confirm.configure(text="Fijar Stock", style="primary")

    def render_view(self):
        self.relleno_superior.pack(side="top")
        self.label_alerta.pack()
        self.sub_label_alerta.pack()

        self.radio_add.grid(row=0, column=0, padx=10)
        self.radio_sub.grid(row=0, column=1, padx=10)
        self.radio_set.grid(row=0, column=2, padx=10)
        self.mode_frame.pack(pady=10)

        self.label_input.grid(row=0, column=0, padx=(0, 8))
        self.entry.grid(row=0, column=1)
        self.input_frame.pack(pady=5)

        self.button_cancel.grid(row=0, column=0, padx=15)
        self.button_confirm.grid(row=0, column=1, padx=15)
        self.buttons_frame.pack(pady=12)

        self.increment_frame.place(relx=0.99, rely=0.017, anchor="ne")

        self.update_idletasks()
        self.table.place(
            relx=0.5,
            y=self.buttons_frame.winfo_y() + self.buttons_frame.winfo_reqheight() + 10,
            relwidth=0.8,
            relheight=0.4,
            anchor="n",
        )
        self.table.render_only_table()
        self.entry.focus_set()

        self.controller.get_products_to_edit()

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        self.confirmar()

    def confirmar(self):
        self.controller.confirmar_cambios(self.stock_var.get(), mode=self.mode_var.get())

    def cambios_realizados(self):
        self.destroy()
        self.parent.realizar_busqueda()

    def cancelar(self):
        self.destroy()
        self.parent.realizar_busqueda()
