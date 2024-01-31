import ttkbootstrap as ttk
import project_functions


# alpha 0.0.9

def abrir_ventana_alerta(parent_window, success, error_type=0):
    def aceptar():
        alert_window.destroy()
        parent_window.focus_set()
        parent_window.actual_focus = 0
        parent_window.entrys[0].focus_set()
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
    alert_window.iconbitmap(parent_window.parent.icon_path)

    # label

    label_alerta = ttk.Label(master=alert_window, text='Algo malio sal :(')
    if success:
        label_alerta = ttk.Label(master=alert_window, text='producto agregado exitosamente')
    label_alerta.configure(font='Arial 20 bold')

    msg = ttk.StringVar()
    label_msg = ttk.Label(master=alert_window, textvariable=msg, font='Arial 12 bold', wraplength=250)

    match error_type:
        case 1:
            msg.set('El campo stock solo debe contener números enteros positivos')
        case 2:
            msg.set('Por favor completá todos los campos con información')
        case 3:
            msg.set('El precio del producto solo puede contener números enteros y el símbolo $')
        case _:
            msg.set('Error desconocido')
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
    def find_focus(self, event):
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
                raise AssertionError('Los campos de datos no pueden estar vacíos')

        return vec_datos

    def add_product(self):
        err = 0
        try:
            datos_producto = self.get_data()
            try:
                exitoso = project_functions.add_to_db(datos_producto)
            except ValueError:
                exitoso = False
                err = 1
            except SyntaxError:
                exitoso = False
                err = 3
            abrir_ventana_alerta(self, exitoso, err)
        except AssertionError:
            abrir_ventana_alerta(self, success=False, error_type=2)

    def nuevo(self):
        self.product_name.set('')
        self.product_code.set('')
        self.product_price.set('$')
        self.product_details.set('')
        self.product_bar_code.set('')
        self.product_stock.set('1')
        self.actual_focus = 0
        self.entrys[0].focus_set()

    # ------------------------------ ventana Principal de la clase (método init) -----------------------------------
    def __init__(self, parent):
        super().__init__()
        # -------------------------------------- atributos principales ---------------------------------------------
        self.parent = parent
        self.actual_focus = 0
        # ----------------------------------------- ventana ---------------------------------------------
        resolution = project_functions.calcular_res_ventana()
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Busqueda de productos')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.geometry(resolution[0])
        self.state('zoomed')
        self.iconbitmap(parent.icon_path)

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
        product_name_entry.focus_set()
        product_code_entry = ttk.Entry(master=input_frame, textvariable=self.product_code, width=30)
        product_price_entry = ttk.Entry(master=input_frame, textvariable=self.product_price, width=30)
        product_details_entry = ttk.Entry(master=input_frame, textvariable=self.product_details, width=30)
        product_bar_code_entry = ttk.Entry(master=input_frame, textvariable=self.product_bar_code, width=30)
        product_stock_entry = ttk.Entry(master=input_frame, textvariable=self.product_stock, width=30)

        self.entrys = [product_name_entry, product_code_entry, product_price_entry,
                       product_details_entry, product_stock_entry, product_bar_code_entry]
        # ----------------------------labels----------------------------
        label_name = ttk.Label(master=input_frame, text='                     Nombre:', anchor='e', font='arial 13')
        label_code = ttk.Label(master=input_frame, text='                     Codigo:', anchor='e', font='arial 13')
        label_price = ttk.Label(master=input_frame, text='                     Precio:', anchor='e', font='arial 13')
        label_details = ttk.Label(master=input_frame, text='                    Detalle:', anchor='e', font='arial 13')
        label_bar_code = ttk.Label(master=input_frame, text='      Codigo de barras:', anchor='e', font='arial 13')
        label_stock = ttk.Label(master=input_frame, text='                      Stock:', anchor='e', font='arial 13')
        label_msg = ttk.Label(master=input_frame, text='Ingrese los datos del producto', font='Arial 14 bold')

        self.labels = [label_name, label_code, label_price, label_details, label_stock, label_bar_code]

        # ----------------------------buttons---------------------------
        button_theme = ttk.Button(master=self, textvariable=parent.str_modo, width=17, style='my.TButton',
                                  command=lambda: project_functions.cambiar_modo
                                  (project_functions.obtener_config('tema'), self.parent, parent.str_modo))

        button_add = ttk.Button(master=input_frame, text='Agregar producto', width=18, style='success',
                                command=self.add_product)

        button_new = ttk.Button(master=input_frame, text='Nuevo', width=18, style='warning', command=self.nuevo)

        menu_button = ttk.Button(master=self, text='Volver al menú',  width=17, style='my.TButton',
                                 command=lambda: project_functions.volver_al_menu(self, self.parent))
        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<KeyRelease>", self.change_focus)
        self.entrys[0].bind('<FocusOut>', self.find_focus)
        self.entrys[1].bind('<FocusOut>', self.find_focus)
        self.entrys[2].bind('<FocusOut>', self.find_focus)
        self.entrys[3].bind('<FocusOut>', self.find_focus)
        self.entrys[4].bind('<FocusOut>', self.find_focus)
        self.entrys[5].bind('<FocusOut>', self.find_focus)
        # ---------------------------------------------- placing widgets -----------------------------------------------
        button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')
        menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        label_msg.grid(row=0, column=1, pady=6)
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i + 1, column=0)
        for i in range(len(self.entrys)):
            self.entrys[i].grid(row=i + 1, column=1, pady=6)
        button_add.grid(row=3, column=2, padx=20)
        button_new.grid(row=4, column=2, padx=20)
        input_frame.place(relx=0.5, rely=0.5, anchor='center')
