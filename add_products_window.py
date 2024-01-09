import ttkbootstrap as ttk
import project_functions


# alpha 0.0.8

def abrir_ventana_alerta(parent_window, success, error_type=0):
    def aceptar():
        alert_window.destroy()
        parent_window.grab_set()
        return

    ancho = int(parent_window.winfo_width() / 4)
    alto = int(parent_window.winfo_height() / 6)
    x = (parent_window.winfo_screenwidth() - ancho) // 2
    y = (parent_window.winfo_screenheight() - alto) // 2

    # ventana

    alert_window = ttk.Toplevel(parent_window)
    alert_window.title('alerta - Error')
    if success:
        alert_window.title('alerta - Producto agregado exitosamente')
    alert_window.geometry(f'{ancho}x{alto}+{x}+{y}')
    alert_window.focus_set()
    alert_window.grab_set()

    # label

    label_alerta = ttk.Label(master=alert_window, text='Algo malio sal :(')
    if success:
        label_alerta = ttk.Label(master=alert_window, text='producto agregado exitosamente')
    label_alerta.configure(font='Arial 20 bold')

    msg = ttk.StringVar(value='Error desconocido')
    label_msg = ttk.Label(master=alert_window, textvariable=msg, font='Arial 12 bold', wraplength=250)

    match error_type:
        case 1:
            msg.set('El campo stock solo debe contener números enteros positivos')
        case 2:
            msg.set('Por favor completá todos los campos con información')
        case _:
            pass
    # confirm_button

    button_confirm = ttk.Button(master=alert_window, text='Aceptar', style='success')
    button_confirm.configure(width=15, command=aceptar)

    # widget placing

    label_alerta.pack()
    button_confirm.place(relx=0.5, rely=0.8, anchor='center', width=100, height=40)
    if not success:
        label_msg.pack()
    # gestion de eventos

    alert_window.bind('<Return>', lambda *args: aceptar())

    # mainloop

    alert_window.mainloop()


class VentAdd(ttk.Toplevel):
    # ----------------------------------------- Métodos de esta clase ---------------------------------------------
    def get_data(self):
        nombre = self.product_name.get()
        codigo = self.product_code.get()
        precio = self.product_price.get()
        detalles = self.product_details.get()
        codigo_barras = self.product_bar_code.get()
        stock = self.product_stock.get()
        vec_datos = [nombre, codigo, precio, detalles, codigo_barras, stock]

        for dato in vec_datos:
            if dato == '':
                raise ValueError('Los campos de datos no pueden estar vacíos')

        return vec_datos

    def add_product(self):
        try:
            datos_producto = self.get_data()
            exitoso = project_functions.add_to_db(datos_producto)
            err = 0
            if not exitoso:
                err = 1
            abrir_ventana_alerta(self, exitoso, err)

        except ValueError:
            abrir_ventana_alerta(self, success=False, error_type=2)

    def nuevo(self):
        self.product_name.set('')
        self.product_code.set('')
        self.product_price.set('$')
        self.product_details.set('')
        self.product_bar_code.set('')
        self.product_stock.set('1')

    # ------------------------------ ventana Principal de la clase (método init) -----------------------------------
    def __init__(self, parent, str_modo_in):
        super().__init__()
        # -------------------------------------- atributos principales ---------------------------------------------
        self.parent = parent
        self.str_modo_in = str_modo_in
        # ----------------------------------------- ventana ---------------------------------------------
        resolution = project_functions.calcular_res_ventana()
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Busqueda de productos')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.geometry(resolution[0])
        self.state('zoomed')

        # -----------------------------------------ttk_variables-----------------------------------------
        self.product_name = ttk.StringVar()
        self.product_code = ttk.StringVar()
        self.product_price = ttk.StringVar(value='$')
        self.product_details = ttk.StringVar()
        self.product_bar_code = ttk.StringVar()
        self.product_stock = ttk.StringVar(value='1')

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # -----------------------------frames---------------------------
        input_frame = ttk.Frame(master=self)

        # ----------------------------entry's---------------------------
        product_name_entry = ttk.Entry(master=input_frame, textvariable=self.product_name, width=30)
        product_code_entry = ttk.Entry(master=input_frame, textvariable=self.product_code, width=30)
        product_price_entry = ttk.Entry(master=input_frame, textvariable=self.product_price, width=30)
        product_details_entry = ttk.Entry(master=input_frame, textvariable=self.product_details, width=30)
        product_bar_code_entry = ttk.Entry(master=input_frame, textvariable=self.product_bar_code, width=30)
        product_stock_entry = ttk.Entry(master=input_frame, textvariable=self.product_stock, width=30)

        # ----------------------------labels----------------------------
        label_name = ttk.Label(master=input_frame, text='                     Nombre:', anchor='e', font='arial 13')
        label_code = ttk.Label(master=input_frame, text='                     Codigo:', anchor='e', font='arial 13')
        label_price = ttk.Label(master=input_frame, text='                     Precio:', anchor='e', font='arial 13')
        label_details = ttk.Label(master=input_frame, text='                    Detalle:', anchor='e', font='arial 13')
        label_bar_code = ttk.Label(master=input_frame, text='      Codigo de barras:', anchor='e', font='arial 13')
        label_stock = ttk.Label(master=input_frame, text='                      Stock:', anchor='e', font='arial 13')
        label_msg = ttk.Label(master=input_frame, text='Ingrese los datos del producto', font='Arial 14 bold')

        # ----------------------------buttons---------------------------
        button_theme = ttk.Button(master=self, textvariable=str_modo_in,
                                  command=lambda: project_functions.cambiar_modo
                                  (project_functions.obtener_config('tema'), self.parent, str_modo_in))

        button_add = ttk.Button(master=input_frame, text='Agregar producto', width=18, style='success',
                                command=self.add_product)

        button_new = ttk.Button(master=input_frame, text='Nuevo', width=18, style='warning', command=self.nuevo)

        menu_button = ttk.Button(master=self, text='Volver al menú',
                                 command=lambda: project_functions.volver_al_menu(self, self.parent))
        # -----------------------------------------------gestion de eventos----------------------------------------

        # none

        # ---------------------------------------------- placing widgets -----------------------------------------------
        button_theme.place(relx=0.990, rely=0.017, anchor='ne')
        menu_button.place(x=15, y=15, anchor='nw')
        label_msg.grid(row=0, column=1, pady=6)
        label_name.grid(row=1, column=0)
        label_code.grid(row=2, column=0)
        label_price.grid(row=3, column=0)
        label_details.grid(row=4, column=0)
        label_stock.grid(row=5, column=0)
        label_bar_code.grid(row=6, column=0)
        product_name_entry.grid(row=1, column=1, pady=6)
        product_code_entry.grid(row=2, column=1, pady=6)
        product_price_entry.grid(row=3, column=1, pady=6)
        product_details_entry.grid(row=4, column=1, pady=6)
        product_stock_entry.grid(row=5, column=1, pady=6)
        product_bar_code_entry.grid(row=6, column=1, pady=6)
        button_add.grid(row=3, column=2, padx=20)
        button_new.grid(row=4, column=2, padx=20)
        input_frame.place(relx=0.5, rely=0.5, anchor='center')
