import ttkbootstrap as ttk


class ProductEntryFields(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.actual_focus = 0

        # -----------------------------------------ttk_variables-----------------------------------------
        self.product_name = ttk.StringVar()
        self.product_code = ttk.StringVar()
        self.product_price = ttk.StringVar(value='$')
        self.product_details = ttk.StringVar()
        self.product_bar_code = ttk.StringVar()
        self.product_stock = ttk.StringVar()

        self.entry_values = [self.product_name, self.product_code, self.product_price,
                             self.product_details, self.product_bar_code, self.product_stock]

        # ----------------------------entry's---------------------------

        self.product_name_entry = ttk.Entry(master=self, textvariable=self.product_name, width=30)
        self.product_name_entry.focus_set()
        self.product_code_entry = ttk.Entry(master=self, textvariable=self.product_code, width=30)
        self.product_price_entry = ttk.Entry(master=self, textvariable=self.product_price, width=30)
        self.product_details_entry = ttk.Entry(master=self, textvariable=self.product_details, width=30)
        self.product_bar_code_entry = ttk.Entry(master=self, textvariable=self.product_bar_code, width=30)
        self.product_stock_entry = ttk.Entry(master=self, textvariable=self.product_stock, width=30)

        self.entries = [self.product_name_entry, self.product_code_entry, self.product_price_entry,
                        self.product_details_entry, self.product_stock_entry, self.product_bar_code_entry]

        # ------- Focus set ---------
        self.product_name_entry.focus_set()

        # ----------------------------labels----------------------------
        self.label_name = ttk.Label(master=self, text='Nombre:'.rjust(28), anchor='e', font='arial 13')
        self.label_code = ttk.Label(master=self, text='Código:'.rjust(28), anchor='e', font='arial 13')
        self.label_price = ttk.Label(master=self, text='Precio:'.rjust(28), anchor='e', font='arial 13')
        self.label_details = ttk.Label(master=self, text='Detalle:'.rjust(28), anchor='e', font='arial 13')
        self.label_bar_code = ttk.Label(master=self, text='Código de barras:'.rjust(21), anchor='e', font='arial 13')
        self.label_stock = ttk.Label(master=self, text='Stock:'.rjust(28), anchor='e', font='arial 13')

        self.labels = [self.label_name, self.label_code, self.label_price,
                       self.label_details, self.label_stock, self.label_bar_code]

        # ----------------------------buttons---------------------------
        self.button_add = ttk.Button(master=self, text='Guardar Producto', width=18, style='success',
                                     command=self.parent.entry_field_accept)

        self.button_new = ttk.Button(master=self, text='Restablecer datos',
                                     width=18, style='warning', command=self.reset_input_fields)

        # -----------------------------------------------gestion de eventos----------------------------------------

        self.entries[0].bind('<FocusOut>', self.find_focus)
        self.entries[1].bind('<FocusOut>', self.find_focus)
        self.entries[2].bind('<FocusOut>', self.find_focus)
        self.entries[3].bind('<FocusOut>', self.find_focus)
        self.entries[4].bind('<FocusOut>', self.find_focus)
        self.entries[5].bind('<FocusOut>', self.find_focus)

    def reset_input_fields(self):
        self.product_name.set('')
        self.product_code.set('')
        self.product_price.set('$')
        self.product_details.set('')
        self.product_bar_code.set('')
        self.product_stock.set('1')
        self.actual_focus = 0
        self.entries[0].focus_set()

    def render(self):
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i + 1, column=0)
        for i in range(len(self.entries)):
            self.entries[i].grid(row=i + 1, column=1, pady=6)
        self.button_add.grid(row=3, column=2, padx=20)
        self.button_new.grid(row=4, column=2, padx=20)

    def show_product(self, producto):
        self.product_name.set(producto.nombre)
        self.product_code.set(producto.codigo)
        self.product_price.set(producto.precio)
        self.product_details.set(producto.detalle)
        self.product_bar_code.set(producto.codigo_de_barras)
        self.product_stock.set(producto.stock)

    def get_entry_data(self) -> dict:
        entry_data = {
            'nombre': self.product_name.get(),
            'codigo': self.product_code.get(),
            'precio': self.product_price.get(),
            'stock': self.product_stock.get(),
            'detalle': self.product_details.get(),
            'codigo_de_barras': self.product_bar_code.get()
        }
        return entry_data

    def find_focus(self, _event):
        if self.entries[self.actual_focus] == self.focus_get():
            return
        for i in range(len(self.entries)):
            if self.focus_get() == self.entries[i]:
                self.actual_focus = i
                return

    def change_focus(self, event):
        if event.keysym == 'Down':
            try:
                if self.actual_focus == len(self.entries) - 1:
                    raise IndexError
                self.actual_focus += 1
                self.entries[self.actual_focus].focus_set()
            except IndexError:
                self.actual_focus = 0
                self.entries[self.actual_focus].focus_set()
        elif event.keysym == 'Up':
            try:
                self.actual_focus -= 1
                if self.actual_focus < 0:
                    raise IndexError
                self.entries[self.actual_focus].focus_set()
            except IndexError:
                self.actual_focus = len(self.entries) - 1
                self.entries[self.actual_focus].focus_set()

    def restart_focus(self):
        self.actual_focus = 0
        self.entries[0].focus_set()