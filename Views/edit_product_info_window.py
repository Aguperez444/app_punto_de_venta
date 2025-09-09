import ttkbootstrap as ttk
import project_functions
from tkinter import messagebox
from Views.base_window_toplevel import BaseProjectWindowToplevel

# Beta 0.1.1


class CRUDWindow(BaseProjectWindowToplevel):
    def aceptar(self):
        new_data = []
        for dato in self.vars:
            new_data.append(dato.get())
        try:
            project_functions.update_info_product_bdd(self.producto[0], new_data)
            self.destroy()
            self.parent.realizar_busqueda()
        except SyntaxError:
            messagebox.showinfo('Error en el precio', 'El precio solo puede ser un número entero')
        except ValueError:
            messagebox.showinfo('Error en el stock', 'El stock solo puede ser un número entero')

    def cancelar(self):
        self.destroy()
        self.parent.realizar_busqueda()

    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")

    def reset_input_fields(self):
        self.product_name.set('')
        self.product_code.set('')
        self.product_price.set('$')
        self.product_details.set('')
        self.product_bar_code.set('')
        self.product_stock.set('1')
        self.actual_focus = 0
        self.entrys[0].focus_set()

    def __init__(self, parent, mod_ids_in):
        super().__init__(parent)
        # -------------------------------------- atributos principales ---------------------------------------------
        self.actual_focus = 0
        self.mod_ids_in = mod_ids_in
        # ----------------------------------------- ventana ---------------------------------------------
        self.ancho = int(parent.winfo_width() / 1.2)
        self.alto = int(parent.winfo_height() / 1.2)
        self.x = (self.winfo_screenwidth() - self.ancho) // 2
        self.y = (self.winfo_screenheight() - self.alto) // 2
        self.title('Cambiar información del producto seleccionado')
        self.geometry=f'{self.ancho}x{self.alto}+{self.x}+{self.y}'
        self.focus_set()

        self.producto = project_functions.busqueda_multiples_ids(mod_ids_in) #TODO CHECK THIS

        # -----------------------------------------ttk_variables-----------------------------------------
        print(self.producto)
        self.product_name = ttk.StringVar()
        self.product_name.set(self.producto[0][1])
        self.product_code = ttk.StringVar()
        self.product_code.set(self.producto[0][2])
        self.product_price = ttk.StringVar(value='$')
        self.product_price.set(self.producto[0][3])
        self.product_details = ttk.StringVar()
        self.product_details.set(self.producto[0][4])
        self.product_bar_code = ttk.StringVar()
        self.product_bar_code.set(self.producto[0][5])
        self.product_stock = ttk.StringVar()
        self.product_stock.set(self.producto[0][6])

        self.vars = [self.product_name, self.product_code, self.product_price,
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
        self.label_bar_code = ttk.Label(master=self.input_frame, text='Código de barras:'.rjust(21), anchor='e', font='arial 13')
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

        self.sub_frame = ttk.Frame(master=self, width=1000, height=12)

        # ----------------------------Ejecutar al abrir---------------------------

        self.pasar_al_cuadro(self.producto)

        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<Configure>", self.on_resize)
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------

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
        self.cuadro.pack_configure(fill='x')
        self.update()
        self.sub_frame.place(relx=0.5, y=self.sub_label_2.winfo_y() + self.sub_label_2.winfo_reqheight() + 5, relwidth=0.8,
                           height=75, anchor='n')
        self.button_cancel.place(relx=0.5, rely=0.99, height=40, width=200, anchor='s')


class VentanaEditInfo(BaseProjectWindowToplevel):

    def __init__(self, parent):
        super().__init__(parent)
        # ----------------------------------------- ventana ---------------------------------------------
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Editar info productos')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.attributes('-zoomed', True)

        # -----------------------------------------------frames---------------------------------------------------

        # Esta clase no implementa frames propios

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()
        self.order_mode = ttk.IntVar()
        # -----------------------------------------simple_variables------------------------------------------------

        # Esta clase no implementa variables simples

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # Esta clase no implementa widgets bootstrap propios

        # --------------------------- buttons --------------------------

        #esta clase no implementa botones propios

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=self.frame, textvariable=self.str_buscado, width=105)

        # --------------------------- labels ---------------------------
        self.label_titulo = ttk.Label(master=self.frame, text='Editar productos', font='Calibri 24 bold')


        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)
        self.cuadro.bind("<Return>", self.edit_selected)
        self.cuadro.bind("<Double-1>", self.edit_selected)
        self.str_buscado.trace_add('write', lambda *args: self.realizar_busqueda()) #TODO CHECK THIS
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        self.frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        self.label_titulo.pack_configure(pady=10)
        self.checkbutton.pack_configure(pady=10)
        self.entry.pack_configure(pady=10, fill='x', expand=True)
        self.cuadro.pack_configure(fill='both', expand=True)
        self.sub_frame.pack_configure(fill='both', expand=True)
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')

        # se ejecuta instantáneamente
        self.pasar_al_cuadro(project_functions.get_all())


    def edit_selected(self, event):
        mod_ids = []
        tuple_items = self.cuadro.selection()
        for item in tuple_items:
            valores = self.cuadro.item(item, option='values')
            mod_ids.append(valores[4])
        CRUDWindow(self, mod_ids)

    def realizar_busqueda(self):
        a = project_functions.busqueda(self.str_buscado)
        if a:
            if self.order_mode.get() == 1:
                a.sort(key=lambda x: x[1])
            project_functions.pasar_al_cuadro(a, self.cuadro)
        else:
            self.cuadro.delete(*self.cuadro.get_children())
            if self.str_buscado.get() == '':
                a = project_functions.get_all()
                if self.order_mode.get() == 1:
                    a.sort(key=lambda x: x[1])
                project_functions.pasar_al_cuadro(a, self.cuadro)

    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")

