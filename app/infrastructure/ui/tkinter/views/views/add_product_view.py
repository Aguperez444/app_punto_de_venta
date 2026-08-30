import ttkbootstrap as ttk
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectView
from app.infrastructure.ui.tkinter.custom_widgets.productEntryFields import ProductEntryFields

from app.infrastructure.ui.tkinter.controllers.actions.add_product_controller import AddProductController


class AddProductsView(BaseProjectView):

    # ------------------------------ Ventana Principal de la clase (init) -----------------------------------
    def __init__(self, master):
        super().__init__(master)
        self.alert_window = None
        self.controller = AddProductController(self)

        self.product_entry_fields = ProductEntryFields(self)

        self.msg_frame = ttk.Frame(master=self)
        self.label_msg = ttk.Label(master=self.msg_frame, text="Ingrese los datos del producto", font="Arial 14 bold")
        self.label_hint = ttk.Label(
            master=self.msg_frame,
            text="Use ↑ / ↓ para cambiar de campo y Enter para guardar el producto",
            font="Arial 10 italic",
        )

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.parent.bind("<KeyRelease>", self.key_released)
        for entry in self.product_entry_fields.entries:
            entry.bind("<Return>", self._on_enter_pressed)
            entry.bind("<KP_Enter>", self._on_enter_pressed)
        self.bind("<Destroy>", self._cleanup_bindings)
        self.controller.finished_init()

    def render_view(self):
        self.button_theme.place(relx=0.990, y=14, anchor="ne")
        self.menu_button.place(x=15, y=14, anchor="nw")
        self.label_msg.grid(row=0, column=1, pady=(10, 2))
        self.label_hint.grid(row=1, column=1, pady=(0, 8))
        self.msg_frame.pack()
        self.product_entry_fields.render()
        self.product_entry_fields.pack()

    def _on_enter_pressed(self, _event=None):
        if not self.winfo_exists():
            return None
        self.entry_field_accept()
        return "break"

    def key_released(self, event):
        if not self.winfo_exists():
            return
        if event.keysym == "Escape":
            self.volver_al_menu()
        elif event.keysym in ("Up", "Down"):
            self.product_entry_fields.change_focus(event)

    def _cleanup_bindings(self, event=None):
        if event is not None and event.widget is not self:
            return
        try:
            self.parent.unbind("<KeyRelease>")
        except Exception:
            pass

    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self._cleanup_bindings()
        super().volver_al_menu(_varname=_varname, _index=_index, _mode=_mode)

    def cerrar_ventana_alerta(self):
        if self.alert_window is not None:
            self.alert_window.destroy()
            self.alert_window = None
        self.focus_set()
        self.product_entry_fields.restart_focus()
        self.grab_set()

    def entry_field_accept(self):
        self.product_data_acquired()

    def product_data_acquired(self):
        datos_producto = self.product_entry_fields.get_entry_data()
        self.controller.add_product(datos_producto)

    def show_success_message(self):
        self.show_message("Producto agregado con éxito")

    def show_error_message(self, msg):
        self.show_error(msg)
