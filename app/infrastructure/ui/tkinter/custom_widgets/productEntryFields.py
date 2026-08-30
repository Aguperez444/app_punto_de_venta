from __future__ import annotations

import ttkbootstrap as ttk

from app.domain.custom_errors import DomainValidationError
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock


class ProductEntryFields(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.actual_focus = 0

        self.product_name = ttk.StringVar()
        self.product_code = ttk.StringVar()
        self.product_price = ttk.StringVar(value="$")
        self.product_details = ttk.StringVar()
        self.product_stock = ttk.StringVar(value="0")
        self.product_bar_code = ttk.StringVar()
        self.validation_msg = ttk.StringVar(value="")

        self.entry_values = [
            self.product_name,
            self.product_code,
            self.product_price,
            self.product_details,
            self.product_stock,
            self.product_bar_code,
        ]

        self.product_name_entry = ttk.Entry(master=self, textvariable=self.product_name, width=32)
        self.product_code_entry = ttk.Entry(master=self, textvariable=self.product_code, width=32)
        self.product_price_entry = ttk.Entry(master=self, textvariable=self.product_price, width=32)
        self.product_details_entry = ttk.Entry(master=self, textvariable=self.product_details, width=32)
        self.product_stock_entry = ttk.Entry(master=self, textvariable=self.product_stock, width=32)
        self.product_bar_code_entry = ttk.Entry(master=self, textvariable=self.product_bar_code, width=32)

        self.entries = [
            self.product_name_entry,
            self.product_code_entry,
            self.product_price_entry,
            self.product_details_entry,
            self.product_stock_entry,
            self.product_bar_code_entry,
        ]

        self.product_name_entry.focus_set()

        self.label_name = ttk.Label(master=self, text="Nombre (*):".rjust(26), anchor="e", font="arial 13")
        self.label_code = ttk.Label(master=self, text="Código (*):".rjust(26), anchor="e", font="arial 13")
        self.label_price = ttk.Label(master=self, text="Precio (*):".rjust(26), anchor="e", font="arial 13")
        self.label_details = ttk.Label(master=self, text="Detalle (opcional):".rjust(26), anchor="e", font="arial 13")
        self.label_stock = ttk.Label(master=self, text="Stock (*):".rjust(26), anchor="e", font="arial 13")
        self.label_bar_code = ttk.Label(
            master=self, text="Código de barras (opc.):".rjust(26), anchor="e", font="arial 13"
        )
        self.label_validation = ttk.Label(
            master=self, textvariable=self.validation_msg, font="arial 10 italic", bootstyle="danger"
        )

        self.labels = [
            self.label_name,
            self.label_code,
            self.label_price,
            self.label_details,
            self.label_stock,
            self.label_bar_code,
        ]

        self.button_add = ttk.Button(
            master=self,
            text="Guardar Producto",
            width=18,
            style="success",
            command=self.parent.entry_field_accept,
        )
        self.button_new = ttk.Button(
            master=self,
            text="Restablecer datos",
            width=18,
            style="warning",
            command=self.reset_input_fields,
        )

        for entry in self.entries:
            entry.bind("<FocusOut>", self.find_focus)

    def validate_inline(self) -> list[str]:
        """Valida los campos requeridos y retorna la lista de errores detectados."""
        errors: list[str] = []
        data = self.get_entry_data()
        if not data["nombre"].strip():
            errors.append("El nombre es obligatorio.")
        if not data["codigo"].strip():
            errors.append("El código es obligatorio.")
        try:
            Precio.from_string(data["precio"])
        except DomainValidationError:
            errors.append("El precio no tiene un formato válido (ej: $150,50).")
        try:
            Stock.from_string(data["stock"])
        except DomainValidationError:
            errors.append("El stock debe ser un número entero.")

        self.validation_msg.set(" ".join(errors))
        return errors

    def reset_input_fields(self):
        self.product_name.set("")
        self.product_code.set("")
        self.product_price.set("$")
        self.product_details.set("")
        self.product_bar_code.set("")
        self.product_stock.set("0")
        self.validation_msg.set("")
        self.actual_focus = 0
        self.entries[0].focus_set()

    def render(self):
        for i, label in enumerate(self.labels):
            label.grid(row=i + 1, column=0, padx=(0, 8))
        for i, entry in enumerate(self.entries):
            entry.grid(row=i + 1, column=1, pady=6)
        self.label_validation.grid(row=len(self.entries) + 1, column=0, columnspan=3, pady=(4, 0))
        self.button_add.grid(row=3, column=2, padx=20)
        self.button_new.grid(row=4, column=2, padx=20)

    def show_product(self, producto):
        self.product_name.set(producto.nombre)
        self.product_code.set(producto.codigo)
        self.product_price.set(str(producto.precio))
        self.product_details.set(producto.detalle or "")
        self.product_bar_code.set(producto.codigo_de_barras or "")
        self.product_stock.set(str(producto.stock))
        self.validation_msg.set("")

    def get_entry_data(self) -> dict:
        return {
            "nombre": self.product_name.get().strip(),
            "codigo": self.product_code.get().strip(),
            "precio": self.product_price.get().strip(),
            "stock": self.product_stock.get().strip(),
            "detalle": self.product_details.get().strip(),
            "codigo_de_barras": self.product_bar_code.get().strip(),
        }

    def find_focus(self, _event):
        if self.entries[self.actual_focus] == self.focus_get():
            return
        for i, entry in enumerate(self.entries):
            if self.focus_get() == entry:
                self.actual_focus = i
                return

    def change_focus(self, event):
        if not self.winfo_exists():
            return
        if event.keysym == "Down":
            self.actual_focus = (self.actual_focus + 1) % len(self.entries)
            target = self.entries[self.actual_focus]
            if target.winfo_exists():
                target.focus_set()
        elif event.keysym == "Up":
            self.actual_focus = (self.actual_focus - 1) % len(self.entries)
            target = self.entries[self.actual_focus]
            if target.winfo_exists():
                target.focus_set()

    def restart_focus(self):
        self.actual_focus = 0
        self.entries[0].focus_set()
