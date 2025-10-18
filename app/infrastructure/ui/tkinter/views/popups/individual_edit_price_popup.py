import ttkbootstrap as ttk

from app.infrastructure.ui.tkinter.custom_widgets.search_table import SearchTable, IHasTable
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectPopupWindow

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.controllers.individual_action.individual_edit_price_controller import IndividualEditPriceController

class IndividualEditPricePopup(BaseProjectPopupWindow, IHasTable):

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

    def __init__(self, parent, controller: 'IndividualEditPriceController'):

        super().__init__(parent)
        self.controller = controller



        self.title('Actualizar precio manualmente')

        self.focus_set()

        self.minsize(1100, 500)
        self.geometry(self.init_controller.calculate_popup_resolution(self.parent.parent))

        # -----------------------------------------python variables-----------------------------------------
        self.porcentajes = ['0,1', '0,2', '0,5', '1', '1,2', '1,5', '1,9', '2', '2,2', '2,4', '2,5', '3', '5', '7',
                            '10', '15', '20', '25', '50', '75', '100', '-50', 'Personalizado']
        # -----------------------------------------ttk_variables-----------------------------------------
        self.porcentaje_var = ttk.StringVar(value='1')
        self.precio_var = ttk.StringVar(value='$')

        # -----------------------------------------Custom widgets------------------------------------------------
        self._table = SearchTable(self, self.resolution_str, self.resolution, 'Productos seleccionados para el cambio:', 'arial 15 italic')
        # -----------------------------------------bootstrap widgets------------------------------------------------
        #--------------------------- frames --------------------------
        self.input_frame = ttk.Frame(master=self)
        self.increment_frame = ttk.Frame(master=self)
        self.buttons_frame = ttk.Frame(master=self)

        #-------------------------- entries --------------------------

        self.entry = ttk.Entry(master=self.input_frame, textvariable=self.precio_var)


        #--------------------------- labels ---------------------------

        self.label_input = ttk.Label(master=self.input_frame, text='Ingrese el nuevo precio:', font='Arial 12 bold')
        self.label_alerta = ttk.Label(master=self, text='Aumentar precio manualmente',
                                      font='Arial 20 bold', wraplength=550)
        self.sub_label_alerta = ttk.Label(master=self, text='Esto solo va a afectar a los productos seleccionados',
                                          font='arial 15 italic')

        # --------------------------- buttons --------------------------

        self.button_confirm = ttk.Button(master=self.buttons_frame, text='Actualizar precio', style='success')
        self.button_confirm.configure(width=15, command=self.aceptar)
        self.button_cancel = ttk.Button(master=self.buttons_frame, text='Cancelar', style='danger')
        self.button_cancel.configure(width=15, command=self.cancelar)
        self.button_increment = ttk.Button(master=self.increment_frame,
                                           text=f'Incrementar un %{self.porcentaje_var.get()} a el/los '
                                                f'productos seleccionados',
                                           style='warning', command=self.actualizar_percent)

        self.porcentaje_combobox = ttk.Combobox(master=self.increment_frame, textvariable=self.porcentaje_var,
                                                values=self.porcentajes)
        self.porcentaje_combobox.configure(width=3, state='readonly')
        self.porcentaje_combobox.set(self.porcentajes[3])

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.table.adjust_size)
        self.porcentaje_var.trace_add("write", self.actualizar_valor)

        self.relleno_superior = ttk.Frame(self, height=44, width=0)

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        self.aceptar()

    def aceptar(self):
        nuevo_precio_str = self.precio_var.get()
        self.controller.update_price_to_new(nuevo_precio_str)


    def cancelar(self):
        self.controller.cancelar_cambios()

    def actualizar_valor(self, _varname=None, _index=None, _mode=None):
        self.button_increment.config(text=f"Incrementar un %{self.porcentaje_var.get()} a el/los productos seleccionados")

    def actualizar_percent(self):
        porcentaje_str = self.porcentaje_var.get()
        self.controller.update_price_by_percentage(porcentaje_str)


    def render_view(self):
        super().render_view() #TODO ACOMODAR ESTA LLAMADA A SUPER
        self.button_increment.grid(row=0, column=0)
        self.porcentaje_combobox.grid(row=0, column=1)
        self.increment_frame.place(relx=0.99, rely=0.017, anchor='ne')

        self.update() # Asegurarse de que sub_label_2 tenga coordenadas antes de ejecutar la sig. Línea

        self.table.place(relx=0.5, y = self.button_confirm.winfo_y() + 200,
                         relwidth=0.8, relheight=0.4, anchor='n')
        self.table.render_only_table()

        self.realizar_busqueda()
        
    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        self.controller.get_products()
