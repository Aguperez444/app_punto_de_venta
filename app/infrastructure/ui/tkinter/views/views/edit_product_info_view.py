from tkinter import messagebox
import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.controllers.actions.edit_product_info_controller import (
    EditProductInfoController,
)
from app.infrastructure.ui.tkinter.custom_widgets.search_table import (
    IHasTable,
    MixinTableNavigation,
    SearchTable,
)
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView


class EditProductInfoView(BaseProjectView, IHasTable, MixinTableNavigation):
    def __init__(self, parent):
        super().__init__(parent)
        MixinTableNavigation.__init__(self)

        self.show_inactive_var = ttk.BooleanVar(value=False)
        self.controller = EditProductInfoController(self)

        self._table = SearchTable(self, self.resolution_str, self.resolution, "Editar productos")

        self.actions_frame = ttk.Frame(master=self)
        self.check_inactive = ttk.Checkbutton(
            master=self.actions_frame,
            text="Mostrar productos archivados",
            variable=self.show_inactive_var,
            command=self.toggle_alphabetic_search,
        )
        self.button_edit = ttk.Button(
            master=self.actions_frame,
            text="Editar seleccionado",
            bootstyle="primary",
            width=20,
            command=lambda: self.edit_selected(None),
        )
        self.button_delete = ttk.Button(
            master=self.actions_frame,
            text="Eliminar producto",
            bootstyle="danger",
            width=20,
            command=self.delete_selected,
        )
        self.button_restore = ttk.Button(
            master=self.actions_frame,
            text="Reactivar producto",
            bootstyle="success",
            width=20,
            command=self.restore_selected,
        )

        self.bind("<Configure>", self.table.adjust_size)
        self.bind("<Escape>", self.volver_al_menu)
        self.parent.bind("<Down>", self.change_focus_down)
        self.parent.bind("<Up>", self._on_up_press)

        self.controller.finished_init()

    @property
    def table(self) -> "SearchTable":
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
        self.table.place(relx=0.5, rely=0.42, relwidth=0.9, relheight=0.62, anchor="center")
        self.table.render()

        self.check_inactive.grid(row=0, column=0, padx=10)
        self.button_edit.grid(row=0, column=1, padx=8)
        self.button_delete.grid(row=0, column=2, padx=8)
        self.button_restore.grid(row=0, column=3, padx=8)
        self.actions_frame.place(relx=0.5, rely=0.82, anchor="center")

        self.controller.get_all_products(include_inactive=self.show_inactive_var.get())

    def _get_single_selected_id(self) -> int | None:
        mod_ids = []
        for item in self.table.get_selected():
            valores = self.table.get_item_data(item)
            if valores:
                mod_ids.append(int(valores[4]))

        if len(mod_ids) > 1:
            self.show_error("Solo se puede seleccionar un producto a la vez.")
            return None
        if len(mod_ids) == 0:
            self.show_error("No hay ningún producto seleccionado.")
            return None
        return mod_ids[0]

    def edit_selected(self, _event):
        id_producto = self._get_single_selected_id()
        if id_producto is not None:
            self.controller.open_individual_edit_info_window(id_producto)

    def delete_selected(self):
        id_producto = self._get_single_selected_id()
        if id_producto is None:
            return
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro que desea eliminar (archivar) este producto?\n"
            "El historial de ventas previas se mantendrá intacto.",
        )
        if confirm and self.controller.delete_product(id_producto):
            self.toggle_alphabetic_search()

    def restore_selected(self):
        id_producto = self._get_single_selected_id()
        if id_producto is None:
            return
        if self.controller.restore_product(id_producto):
            self.toggle_alphabetic_search()

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        filtro_busqueda = self.table.get_search()
        include_inactive = self.show_inactive_var.get()

        if filtro_busqueda.strip() == "":
            self.controller.get_all_products(include_inactive=include_inactive)
        else:
            self.controller.get_filtered_products(
                filtro_busqueda, include_inactive=include_inactive
            )

    def realizar_busqueda_alfabetica(self):
        filtro_busqueda = self.table.get_search()
        include_inactive = self.show_inactive_var.get()

        if filtro_busqueda.strip() == "":
            self.controller.get_all_products_alphabetically(include_inactive=include_inactive)
        else:
            self.controller.get_filtered_products_alphabetically(
                filtro_busqueda, include_inactive=include_inactive
            )

    def toggle_alphabetic_search(self):
        if self.table.its_alphabetic_checked():
            self.realizar_busqueda_alfabetica()
        else:
            self.realizar_busqueda()

    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self.parent.bind("<Down>", self.clear_event)
        self.parent.bind("<Up>", self.clear_event)
        super().volver_al_menu(_varname=_varname, _index=_index, _mode=_mode)
