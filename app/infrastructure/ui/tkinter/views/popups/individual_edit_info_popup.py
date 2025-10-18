import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import SearchTable, IHasTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectPopupWindow
from app.infrastructure.ui.tkinter.custom_widgets.productEntryFields import ProductEntryFields

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_info_controller import IndividualEditInfoController

class IndividualEditInfoPopup(BaseProjectPopupWindow, IHasTable):
    @property
    def table(self) -> 'SearchTable':
        return self._table

    def table_action(self, event):
        pass

    def entry_action(self, *args):
        pass

    def search_action(self):
        pass

    def alphabetical_search_action(self):
        pass

    def __init__(self, parent, controller: 'IndividualEditInfoController'):
        super().__init__(parent)

        self.controller = controller

        # -------------------------------------- atributos principales ---------------------------------------------
        self.actual_focus = 0
        # ----------------------------------------- ventana ---------------------------------------------



        self.title('Cambiar información del producto seleccionado')
        self.focus_set()
        self.minsize(600, 625)


        # -----------------------------------------Custom widgets-----------------------------------------
        self.product_entry = ProductEntryFields(self)
        self._table = SearchTable(self, self.resolution_str, self.resolution, 'Datos actuales del producto:', 'arial 15 italic')


        # -----------------------------frames---------------------------
        self.buttons_frame = ttk.Frame(master=self)
        self.msg_frame = ttk.Frame(master=self)

        # ----------------------------labels----------------------------

        self.label_msg = ttk.Label(master=self.msg_frame, text='Ingrese los datos del producto', font='Arial 14 bold')

        self.label_alerta = ttk.Label(master=self, text='Actualizar datos del producto',
                                      font='Arial 20 bold', wraplength=550)
        self.sub_label_alerta = ttk.Label(master=self, text='Esto solo va a afectar a el producto seleccionado',
                                          font='arial 15 italic')

        # ----------------------------buttons---------------------------

        self.button_cancel = ttk.Button(master=self, text='Cancelar', style='danger')
        self.button_cancel.configure(width=15, command=self.cancelar)


        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<Configure>", self.table.adjust_size)

        # ---------------------------------------------- placing widgets -----------------------------------------------

    def render_view(self):
        self.label_alerta.pack()
        self.sub_label_alerta.pack()
        self.label_msg.grid(row=0, column=1, pady=6)
        self.msg_frame.pack()
        self.product_entry.render()
        self.product_entry.pack()
        self.buttons_frame.pack(pady=15)

        self.update()

        self.table.place(relx=0.5, y=self.buttons_frame.winfo_y() + self.buttons_frame.winfo_reqheight() + 5,
                             relwidth=0.8, height=155, anchor='n')

        self.table.render_only_table()

        self.update()

        self.button_cancel.place(relx=0.5, y=self.table.winfo_y() + 155 + 15,
                                 height=40, width=200, anchor='n')

        self.controller.get_product_info()



    def mostrar_datos(self, producto):
        self.product_entry.show_product(producto)
        #TODO CHECK THIS, might be better to use DTO


    def confirm_action(self, _varname=None, _index=None, _mode=None):
        self.entry_field_accept()

    def entry_field_accept(self):
        new_data = self.product_entry.get_entry_data()

        self.controller.update_product(new_data)


    def cancelar(self):
        self.controller.cancelar_cambios()


