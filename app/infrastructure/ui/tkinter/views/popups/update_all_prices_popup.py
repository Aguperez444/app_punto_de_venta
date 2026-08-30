from __future__ import annotations

from typing import TYPE_CHECKING
import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import (
    BaseProjectPopupWindow,
)

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.controllers.confirm_action.update_all_prices_controller import (
        UpdateAllPricesController,
    )


class UpdateAllPricesPopup(BaseProjectPopupWindow):
    def __init__(self, parent_window, controller: "UpdateAllPricesController"):
        super().__init__(parent_window, width=560, height=255)
        self.controller = controller

        self.title("Confirmar Actualización de precios")
        self.minsize(520, 235)
        self.resizable(False, False)
        self.center_on_parent(560, 255)

        self.focus_set()
        self.grab_set()

        self.content_frame = ttk.Frame(master=self, padding=(24, 20))
        self.buttons_frame = ttk.Frame(master=self.content_frame)

        pct_display = (
            parent_window.get_effective_percentage_str()
            if hasattr(parent_window, "get_effective_percentage_str")
            else parent_window.porcentaje_var.get()
        )
        self.label_alerta = ttk.Label(
            master=self.content_frame,
            text=f"¿Está seguro que desea aplicar un %{pct_display} a todos los productos?",
            font="Arial 15 bold",
            wraplength=500,
            justify="center",
        )
        self.sub_label_alerta = ttk.Label(
            master=self.content_frame,
            text="Esto va a afectar a TODOS los productos, no solo a los que aparecieron buscados por nombre.",
            font="Arial 11 italic",
            wraplength=480,
            justify="center",
        )
        self.button_confirm = ttk.Button(
            master=self.buttons_frame,
            text="Aceptar",
            bootstyle="warning",
            width=15,
            command=self.aceptar,
        )
        self.button_cancel = ttk.Button(
            master=self.buttons_frame,
            text="Cancelar",
            bootstyle="danger",
            width=15,
            command=self.cancelar,
        )

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        self.aceptar()

    def aceptar(self):
        self.controller.confirmar_cambios()

    def cancelar(self):
        self.controller.cancelar_cambios()

    def render_view(self):
        self.content_frame.pack(fill="both", expand=True)
        self.label_alerta.pack(pady=(6, 10))
        self.sub_label_alerta.pack(pady=(0, 18))
        self.button_cancel.grid(row=0, column=0, padx=12)
        self.button_confirm.grid(row=0, column=1, padx=12)
        self.buttons_frame.pack(pady=(4, 6))
        self.update_idletasks()
        self.center_on_parent(560, max(self.winfo_reqheight() + 10, 245))
