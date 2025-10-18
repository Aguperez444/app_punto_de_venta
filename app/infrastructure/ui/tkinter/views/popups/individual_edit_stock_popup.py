import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import SearchTable, IHasTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectPopupWindow

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_stock_controller import IndividualEditStockController


class IndividualEditStockPopup(BaseProjectPopupWindow, IHasTable):

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

    def __init__(self, parent, controller: 'IndividualEditStockController'):
        super().__init__(parent)
        self.controller = controller
        self.title('Actualizar Stock de productos seleccionados')
        self.focus_set()

        # -----------------------------------------python variables-----------------------------------------

        # -----------------------------------------ttk_variables-----------------------------------------
        self.stock_var = ttk.StringVar(value='')
        # -----------------------------------------Custom widgets-----------------------------------------
        self._table = SearchTable(self, self.resolution_str, self.resolution, 'Productos seleccionados para el cambio:', 'arial 15 italic')

        # -----------------------------------------bootstrap widgets-----------------------------------------

        # -----------------------------------------frames-----------------------------------------

        self.input_frame = ttk.Frame(master=self)
        self.increment_frame = ttk.Frame(master=self)
        self.buttons_frame = ttk.Frame(master=self)

        # ----------------------------------------- entries -----------------------------------------

        self.entry = ttk.Entry(master=self.input_frame, textvariable=self.stock_var)

        # -----------------------------------------labels-----------------------------------------

        self.label_input = ttk.Label(master=self.input_frame, text='Ingrese el stock a agregar:', font='Arial 12 bold')
        self.label_alerta = ttk.Label(master=self, text='Actualizar stock', font='Arial 20 bold', wraplength=550)
        self.sub_label_alerta = ttk.Label(master=self, text='Esto solo va a afectar a los productos seleccionados',
                                     font='arial 15 italic')

        # ----------------------------------------- buttons -----------------------------------------

        self.button_confirm = ttk.Button(master=self.buttons_frame, text='Añadir Stock', style='success')
        self.button_confirm.configure(width=15, command=self.confirmar)
        self.button_cancel = ttk.Button(master=self.buttons_frame, text='Cancelar', style='danger')
        self.button_cancel.configure(width=15, command=self.cancelar)

        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<Configure>", self.table.adjust_size)

        # extras necesarios
        self.relleno_superior = ttk.Frame(self, height=44, width=0)


    def render_view(self):
        super().render_view()
        self.increment_frame.place(relx=0.99, rely=0.017, anchor='ne')

        self.update_idletasks()

        self.table.place(relx=0.5, y= self.button_confirm.winfo_height() + 280, relwidth=0.8, relheight=0.4, anchor="center")
        self.table.render_only_table()

        self.controller.get_products_to_edit()

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        self.confirmar()


    def confirmar(self):
        quantity = int(self.stock_var.get())
        self.controller.confirmar_cambios(quantity)



    def cambios_realizados(self):
        self.destroy()
        self.parent.realizar_busqueda()


    def cancelar(self):
        self.destroy()
        self.parent.realizar_busqueda()
