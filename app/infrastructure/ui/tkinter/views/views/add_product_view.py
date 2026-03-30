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

        # -------------------------------------- Atributos principales ---------------------------------------------

        # -----------------------------Custom Widgets---------------------------

        self.product_entry_fields = ProductEntryFields(self)

        # -----------------------------frames---------------------------

        self.msg_frame = ttk.Frame(master=self)

        # ----------------------------labels----------------------------
        self.label_msg = ttk.Label(master=self.msg_frame, text='Ingrese los datos del producto', font='Arial 14 bold')

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.parent.bind('<KeyRelease>', self.key_released)
        self.controller.finished_init()


    def render_view(self):
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')
        self.menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        self.label_msg.grid(row=0, column=1, pady=6)
        self.msg_frame.pack()
        self.product_entry_fields.render()
        self.product_entry_fields.pack()


    def key_released(self, event):
        if event.keysym == 'Escape':
            self.volver_al_menu()
        else:
            self.product_entry_fields.change_focus(event)


    #TODO CHECK THIS
    def cerrar_ventana_alerta(self):
        self.alert_window.destroy()
        self.alert_window = None
        self.focus_set()
        self.product_entry_fields.restart_focus()
        self.grab_set()
        return


    def entry_field_accept(self):
        self.product_data_acquired()


    def product_data_acquired(self):
        datos_producto = self.product_entry_fields.get_entry_data()

        self.controller.add_product(datos_producto)


    def show_success_message(self):
        self.show_message('Producto agregado con éxito', )


    def show_error_message(self, msg):
        self.show_error(msg)
