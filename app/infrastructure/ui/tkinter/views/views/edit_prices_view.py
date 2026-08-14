from decimal import Decimal, InvalidOperation
import ttkbootstrap as ttk

from app.domain.models.precio import Precio
from app.infrastructure.ui.tkinter.controllers.actions.edit_prices_controller import (
    EditPricesController,
)
from app.infrastructure.ui.tkinter.custom_widgets.search_table import (
    IHasTable,
    MixinTableNavigation,
    SearchTable,
)
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView


class EditPricesView(BaseProjectView, IHasTable, MixinTableNavigation):
    def __init__(self, parent):
        super().__init__(parent)
        MixinTableNavigation.__init__(self)

        self.actual_focus = 0
        self.controller = EditPricesController(self)

        self.increment_frame = ttk.Frame(master=self)

        self.porcentaje_var = ttk.StringVar(value="1")
        self.custom_porcentaje_var = ttk.StringVar(value="")
        self.preview_var = ttk.StringVar(value="")

        self.porcentajes = [
            "0,1", "0,2", "0,5", "1", "1,2", "1,5", "1,9", "2", "2,2", "2,4", "2,5",
            "3", "5", "7", "10", "15", "20", "25", "50", "75", "100", "-50", "Personalizado",
        ]

        self._table = SearchTable(self, self.resolution_str, self.resolution, "Actualización de precios")

        self.button_increment = ttk.Button(
            master=self.increment_frame,
            text=f"Aplicar %{self.porcentaje_var.get()} a todos los precios",
            style="warning",
            command=self.increment_all,
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
        self.preview_label = ttk.Label(
            master=self.increment_frame,
            textvariable=self.preview_var,
            font="Arial 9 italic",
        )

        self.bind("<Configure>", self.table.adjust_size)
        self.porcentaje_var.trace_add("write", self.actualizar_valor)
        self.custom_porcentaje_var.trace_add("write", self.actualizar_valor)

        self.bind("<Escape>", self.volver_al_menu)
        self.parent.bind("<Down>", self.change_focus_down)
        self.parent.bind("<Up>", self._on_up_press)

        self.actualizar_valor()
        self.controller.finished_init()

    @property
    def table(self) -> SearchTable:
        return self._table

    def table_action(self, event):
        self.edit_selected(event)

    def entry_action(self, *args):
        self.toggle_alphabetic_search()

    def search_action(self):
        self.realizar_busqueda()

    def alphabetical_search_action(self):
        self.realizar_busqueda_alfabetica()

    def render_view(self):
        super().render_base()

        self.table.place(relx=0.5, rely=0.43, relwidth=0.9, relheight=0.6, anchor="center")
        self.table.render()

        self.button_increment.grid(row=0, column=0, ipady=3, padx=(0, 6))
        self.porcentaje_combobox.grid(row=0, column=1, ipady=3)
        self.preview_label.grid(row=1, column=0, columnspan=3, sticky="e", pady=(2, 0))
        self.increment_frame.place(relx=0.82, rely=0.012, anchor="ne")

        self.controller.get_all_products()

    def edit_selected(self, _event):
        mod_ids = []
        tuple_items = self.table.get_selected()
        for item in tuple_items:
            valores = self.table.get_item_data(item)
            if valores:
                mod_ids.append(int(valores[4]))

        if mod_ids:
            self.controller.open_individual_edit_price_window(mod_ids)

    def get_effective_percentage_str(self) -> str:
        selected = self.porcentaje_var.get()
        if selected == "Personalizado":
            return self.custom_porcentaje_var.get().strip().replace(",", ".")
        return selected.strip().replace(",", ".")

    def actualizar_valor(self, *_args):
        is_custom = self.porcentaje_var.get() == "Personalizado"
        if is_custom:
            self.custom_percent_entry.grid(row=0, column=2, ipady=3, padx=(6, 0))
            self.custom_percent_entry.focus_set()
        else:
            self.custom_percent_entry.grid_forget()

        raw_pct = self.get_effective_percentage_str()
        display_pct = raw_pct if raw_pct else "..."
        self.button_increment.config(text=f"Aplicar %{display_pct} a todos los precios")

        try:
            pct = Decimal(raw_pct)
            if pct <= Decimal("-100"):
                self.preview_var.set("Porcentaje inválido (debe ser > -100%)")
            else:
                ejemplo = Precio(Decimal("1000.00")).aplicar_porcentaje(pct)
                self.preview_var.set(f"Ej: $1.000,00 → {ejemplo}")
        except (InvalidOperation, ValueError):
            self.preview_var.set("Ingrese un porcentaje numérico (ej: 12,5 o -15)")

    def toggle_alphabetic_search(self):
        if self.table.its_alphabetic_checked():
            self.realizar_busqueda_alfabetica()
        else:
            self.realizar_busqueda()

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        filtro_busqueda = self.table.get_search()
        if filtro_busqueda.strip() == "":
            self.controller.get_all_products()
        else:
            self.controller.get_filtered_products(filtro_busqueda)

    def realizar_busqueda_alfabetica(self):
        filtro_busqueda = self.table.get_search()
        if filtro_busqueda.strip() == "":
            self.controller.get_all_products_alphabetically()
        else:
            self.controller.get_filtered_products_alphabetically(filtro_busqueda)

    def increment_all(self):
        raw_pct = self.get_effective_percentage_str()
        try:
            pct = Decimal(raw_pct)
            if pct <= Decimal("-100"):
                raise ValueError
        except (InvalidOperation, ValueError):
            self.show_error("Ingrese un porcentaje numérico válido mayor a -100%.")
            return
        self.controller.open_update_all_prices_window()

    def confirmar_cambios(self):
        porcentaje_elegido = self.get_effective_percentage_str()
        self.controller.update_all_prices(porcentaje_elegido)

    def cambios_realizados(self, percentage):
        self.show_message(f"Se han actualizado correctamente los precios en un %{percentage}")
        self.toggle_alphabetic_search()

    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self.parent.bind("<Down>", self.clear_event)
        self.parent.bind("<Up>", self.clear_event)
        super().volver_al_menu(_varname=_varname, _index=_index, _mode=_mode)
