import ttkbootstrap as ttk

from Views.base_window_toplevel import BaseProjectWindowToplevel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Controllers.individual_edit_info_controller import IndividualEditInfoController

class IndividualEditPopup(BaseProjectWindowToplevel):
    def __init__(self, parent, controller: 'IndividualEditInfoController'):
        super().__init__(parent)

        self.controller = controller

        # -------------------------------------- atributos principales ---------------------------------------------
        self.actual_focus = 0
        # ----------------------------------------- ventana ---------------------------------------------
        self.ancho = int(parent.winfo_width() / 1.2)
        self.alto = int(parent.winfo_height() / 1.2)
        self.x = (self.winfo_screenwidth() - self.ancho) // 2
        self.y = (self.winfo_screenheight() - self.alto) // 2
        self.title('Cambiar información del producto seleccionado')
        self.geometry(f'{self.ancho}x{self.alto}+{self.x}+{self.y}')
        self.focus_set()


        # -----------------------------------------ttk_variables-----------------------------------------
        self.product_name = ttk.StringVar()
        self.product_code = ttk.StringVar()
        self.product_price = ttk.StringVar(value='$')
        self.product_details = ttk.StringVar()
        self.product_bar_code = ttk.StringVar()
        self.product_stock = ttk.StringVar()


        self.entry_values = [self.product_name, self.product_code, self.product_price,
                             self.product_details, self.product_bar_code, self.product_stock]

        # -----------------------------frames---------------------------
        self.buttons_frame = ttk.Frame(master=self)
        self.input_frame = ttk.Frame(master=self)

        # ----------------------------entry's---------------------------
        self.product_name_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_name, width=30)
        self.product_name_entry.focus_set()
        self.product_code_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_code, width=30)
        self.product_price_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_price, width=30)
        self.product_details_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_details, width=30)
        self.product_bar_code_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_bar_code, width=30)
        self.product_stock_entry = ttk.Entry(master=self.input_frame, textvariable=self.product_stock, width=30)

        self.entrys = [self.product_name_entry, self.product_code_entry, self.product_price_entry,
                       self.product_details_entry, self.product_stock_entry, self.product_bar_code_entry]
        # ----------------------------labels----------------------------
        self.label_name = ttk.Label(master=self.input_frame, text='Nombre:'.rjust(28), anchor='e', font='arial 13')
        self.label_code = ttk.Label(master=self.input_frame, text='Código:'.rjust(28), anchor='e', font='arial 13')
        self.label_price = ttk.Label(master=self.input_frame, text='Precio:'.rjust(28), anchor='e', font='arial 13')
        self.label_details = ttk.Label(master=self.input_frame, text='Detalle:'.rjust(28), anchor='e', font='arial 13')
        self.label_bar_code = ttk.Label(master=self.input_frame, text='Código de barras:'.rjust(21), anchor='e',
                                        font='arial 13')
        self.label_stock = ttk.Label(master=self.input_frame, text='Stock:'.rjust(28), anchor='e', font='arial 13')
        self.label_msg = ttk.Label(master=self.input_frame, text='Ingrese los datos del producto', font='Arial 14 bold')

        self.labels = [self.label_name, self.label_code, self.label_price,
                       self.label_details, self.label_stock, self.label_bar_code]

        self.label_alerta = ttk.Label(master=self, text='Actualizar datos del producto',
                                      font='Arial 20 bold', wraplength=550)
        self.sub_label_alerta = ttk.Label(master=self, text='Esto solo va a afectar a el producto seleccionado',
                                          font='arial 15 italic')
        self.sub_label_2 = ttk.Label(master=self, text='Datos actuales del producto:',
                                     font='arial 15 italic')

        # ----------------------------buttons---------------------------

        self.button_add = ttk.Button(master=self.input_frame, text='Actualizar datos', width=18, style='success',
                                     command=self.aceptar)

        self.button_new = ttk.Button(master=self.input_frame, text='Restablecer datos',
                                     width=18, style='warning', command=self.reset_input_fields)

        self.button_cancel = ttk.Button(master=self, text='Cancelar', style='danger')
        self.button_cancel.configure(width=15, command=self.cancelar)


        # ----------------------------Ejecutar al abrir---------------------------

        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<Configure>", self.on_resize)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------

    def render_view(self):
        self.label_alerta.pack()
        self.sub_label_alerta.pack()
        self.label_msg.grid(row=0, column=1, pady=6)
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i + 1, column=0)
        for i in range(len(self.entrys)):
            self.entrys[i].grid(row=i + 1, column=1, pady=6)
        self.button_add.grid(row=3, column=2, padx=20)
        self.button_new.grid(row=4, column=2, padx=20)
        self.input_frame.pack()
        self.buttons_frame.pack(pady=15)
        self.sub_label_2.pack()
        #self.sub_label_alerta.pack_configure(fill='x')

        self.cuadro.pack_configure(fill='x')
        self.sub_frame.pack_configure(fill='both', expand=True)
        self.update()
        self.frame.place(relx=0.5, y=self.sub_label_2.winfo_y() + self.sub_label_2.winfo_reqheight() + 5,
                             relwidth=0.8,
                             height=75, anchor='n')

        self.button_cancel.place(relx=0.5, rely=0.90, height=40, width=200, anchor='s')

        self.controller.get_product_info()



    def adjust_geometry(self):
        self.update()
        self.geometry(f'{self.ancho}x{self.frame.winfo_y() + self.frame.winfo_reqheight() + 50}+{self.x}+{self.y}')



    def reset_input_fields(self):
        self.product_name.set('')
        self.product_code.set('')
        self.product_price.set('$')
        self.product_details.set('')
        self.product_bar_code.set('')
        self.product_stock.set('1')
        self.actual_focus = 0
        self.entrys[0].focus_set()


    def mostrar_datos(self, producto):
        self.product_name.set(producto.producto)
        self.product_code.set(producto.codigo)
        self.product_price.set(f'${producto.precio}'.replace('.', ','))
        self.product_details.set(producto.detalle)
        self.product_bar_code.set(producto.codigo_de_barras)
        self.product_stock.set(producto.stock)
        #TODO CHECK THIS, might be better to use DTO


    def aceptar(self):
        new_data = {
            'producto': self.product_name.get(),
            'codigo': self.product_code.get(),
            'precio': self.product_price.get(),
            'detalle': self.product_details.get(),
            'codigo_de_barras': self.product_bar_code.get(),
            'stock': self.product_stock.get()
        }

        self.controller.update_product(new_data)


    def cancelar(self):
        self.controller.cancelar_cambios()


