import ttkbootstrap as ttk
from Views.base_window_abstract_class import BaseProjectWindowToplevel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controllers.add_product_controller import AddProductController


#TODO PASAR ESTA VENTANA A UNA CLASE APARTE, PARA QUE NO SE MEZCLEN LOS CÓDIGOS DE LAS VENTANAS


class AddProductsWindow(BaseProjectWindowToplevel):

    # ------------------------------ ventana Principal de la clase (init) -----------------------------------
    def __init__(self, parent, controller: 'AddProductController'):
        self.alert_window = None
        self.add_product_controller = controller
        super().__init__(parent, needs_cuadro=False)
        # -------------------------------------- atributos principales ---------------------------------------------
        self.actual_focus = 0
        # ----------------------------------------- ventana ---------------------------------------------
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Busqueda de productos')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())

        self.maximizar()


        # -----------------------------------------ttk_variables-----------------------------------------
        self.product_name = ttk.StringVar()
        self.product_code = ttk.StringVar()
        self.product_price = ttk.StringVar(value='$')
        self.product_details = ttk.StringVar()
        self.product_bar_code = ttk.StringVar()
        self.product_stock = ttk.StringVar(value='1')

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # -----------------------------frames---------------------------
        self.input_frame = ttk.Frame(master=self)

        # ----------------------------entry's---------------------------
        self.product_name_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_name, width=30)
        self.product_code_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_code, width=30)
        self.product_price_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_price, width=30)
        self.product_details_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_details, width=30)
        self.product_bar_code_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_bar_code, width=30)
        self.product_stock_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_stock, width=30)

        self.entrys = [self.product_name_entry, self.product_code_entry, self.product_price_entry,
                       self.product_details_entry, self.product_stock_entry, self.product_bar_code_entry]

        # ------- Focus set ---------
        self.product_name_entry.focus_set()

        # ----------------------------labels----------------------------
        self.label_name = ttk.Label(master=self.input_frame, text='Nombre:'.rjust(28), anchor='e', font='arial 13')
        self.label_code = ttk.Label(master=self.input_frame, text='Codigo:'.rjust(28), anchor='e', font='arial 13')
        self.label_price = ttk.Label(master=self.input_frame, text='Precio:'.rjust(28), anchor='e', font='arial 13')
        self.label_details = ttk.Label(master=self.input_frame, text='Detalle:'.rjust(28), anchor='e', font='arial 13')
        self.label_bar_code = ttk.Label(master=self.input_frame, text='Codigo de barras:'.rjust(21), anchor='e', font='arial 13') # 21 para que quede alineado con los demás (por alguna razón no se alinea con 28)
        self.label_stock = ttk.Label(master=self.input_frame, text='Stock:'.rjust(28), anchor='e', font='arial 13')
        self.label_msg = ttk.Label(master=self.input_frame, text='Ingrese los datos del producto', font='Arial 14 bold')

        self.labels = [self.label_name, self.label_code, self.label_price, self.label_details, self.label_stock, self.label_bar_code]

        # ----------------------------buttons---------------------------

        self.button_add = ttk.Button(master=self.input_frame, text='Agregar producto', width=18, style='success',
                                     command=self.product_data_acquired)

        self.button_new = ttk.Button(master=self.input_frame, text='Nuevo', width=18, style='warning',
                                     command=self.reset_entry_fields)

        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<KeyRelease>", self.change_focus)
        self.entrys[0].bind('<FocusOut>', self.find_focus)
        self.entrys[1].bind('<FocusOut>', self.find_focus)
        self.entrys[2].bind('<FocusOut>', self.find_focus)
        self.entrys[3].bind('<FocusOut>', self.find_focus)
        self.entrys[4].bind('<FocusOut>', self.find_focus)
        self.entrys[5].bind('<FocusOut>', self.find_focus)



    # ----------------------------------------- Métodos de esta clase ---------------------------------------------
    def render_view(self):
        # ----------------------------------------- Colocación de widgets -----------------------------------------
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')
        self.menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        self.label_msg.grid(row=0, column=1, pady=6)
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i + 1, column=0)
        for i in range(len(self.entrys)):
            self.entrys[i].grid(row=i + 1, column=1, pady=6)
        self.button_add.grid(row=3, column=2, padx=20)
        self.button_new.grid(row=4, column=2, padx=20)
        self.input_frame.place(relx=0.5, rely=0.5, anchor='center')


    def find_focus(self, _event):
        if self.entrys[self.actual_focus] == self.focus_get():
            return
        for i in range(len(self.entrys)):
            if self.focus_get() == self.entrys[i]:
                self.actual_focus = i
                return

    def change_focus(self, event):
        if event.keysym == 'Down':
            try:
                if self.actual_focus == len(self.entrys) - 1:
                    raise IndexError
                self.actual_focus += 1
                self.entrys[self.actual_focus].focus_set()
            except IndexError:
                self.actual_focus = 0
                self.entrys[self.actual_focus].focus_set()
        elif event.keysym == 'Up':
            try:
                self.actual_focus -= 1
                if self.actual_focus < 0:
                    raise IndexError
                self.entrys[self.actual_focus].focus_set()
            except IndexError:
                self.actual_focus = len(self.entrys) - 1
                self.entrys[self.actual_focus].focus_set()

    def get_input_data(self):
        nombre = self.product_name.get()
        codigo = self.product_code.get()
        precio = self.product_price.get()
        detalles = self.product_details.get()
        codigo_barras = self.product_bar_code.get()
        stock = self.product_stock.get()
        dict_datos = {
            'producto': nombre,
            'codigo': codigo,
            'precio': precio,
            'detalle': detalles,
            'codigo_de_barras': codigo_barras,
            'stock': stock
        }

        return dict_datos


    #TODO CHECK THIS
    def cerrar_ventana_alerta(self):
        self.alert_window.destroy()
        self.alert_window = None
        self.focus_set()
        self.actual_focus = 0
        self.entrys[0].focus_set()
        self.grab_set()
        return

    def product_data_acquired(self):
        datos_producto = self.get_input_data()

        for key, value in datos_producto.items():
            if str(value) == '' or str(value).isspace(): # TODO CHECK THIS LATER
                self.show_error("Completá todos los campos")
                return
        self.add_product_controller.add_product(datos_producto)


    def reset_entry_fields(self):
        self.product_name.set('')
        self.product_code.set('')
        self.product_price.set('$')
        self.product_details.set('')
        self.product_bar_code.set('')
        self.product_stock.set('1')
        self.actual_focus = 0
        self.entrys[0].focus_set()

    def show_success_message(self):
        self.show_message('Producto agregado con éxito', )

    def show_error_message(self, msg):
        self.show_error(msg)
