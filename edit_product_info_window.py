import ttkbootstrap as ttk
import project_functions
from tkinter import messagebox

# Beta 0.1.1


class CRUDWindow(ttk.Toplevel):
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

    def nuevo(self):
        self.product_name.set('')
        self.product_code.set('')
        self.product_price.set('$')
        self.product_details.set('')
        self.product_bar_code.set('')
        self.product_stock.set('1')
        self.actual_focus = 0
        self.entrys[0].focus_set()

    def __init__(self, parent, mod_ids_in):
        super().__init__()
        # -------------------------------------- atributos principales ---------------------------------------------
        self.parent = parent
        self.actual_focus = 0
        self.mod_ids_in = mod_ids_in
        # ----------------------------------------- ventana ---------------------------------------------
        ancho = int(parent.winfo_width() / 1.2)
        alto = int(parent.winfo_height() / 1.2)
        x = (parent.winfo_screenwidth() - ancho) // 2
        y = (parent.winfo_screenheight() - alto) // 2
        self.title('Cambiar información del producto seleccionado')
        self.geometry(f'{ancho}x{alto}+{x}+{y}')
        self.state('zoomed')
        self.iconbitmap(parent.parent.icon_path)
        self.focus_set()

        self.producto = project_functions.busqueda_multiples_ids(mod_ids_in)

        # -----------------------------------------ttk_variables-----------------------------------------
        self.product_name = ttk.StringVar()
        self.product_code = ttk.StringVar()
        self.product_price = ttk.StringVar(value='$')
        self.product_details = ttk.StringVar()
        self.product_bar_code = ttk.StringVar()
        self.product_stock = ttk.StringVar()

        self.vars = [self.product_name, self.product_code, self.product_price,
                     self.product_details, self.product_bar_code, self.product_stock]

        # -----------------------------frames---------------------------
        buttons_frame = ttk.Frame(master=self)
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

        label_alerta = ttk.Label(master=self, text='Actualizar datos del producto',
                                 font='Arial 20 bold', wraplength=550)
        sub_label_alerta = ttk.Label(master=self, text='Esto solo va a afectar a el producto seleccionado',
                                     font='arial 15 italic')
        sub_label_2 = ttk.Label(master=self, text='Datos actuales del producto:',
                                font='arial 15 italic')

        # ----------------------------buttons---------------------------

        button_add = ttk.Button(master=input_frame, text='Actualizar datos', width=18, style='success',
                                command=self.aceptar)

        button_new = ttk.Button(master=input_frame, text='Restablecer datos',
                                width=18, style='warning', command=self.nuevo)

        button_cancel = ttk.Button(master=self, text='Cancelar', style='danger')
        button_cancel.configure(width=15, command=self.cancelar)

        frame_cuadro = ttk.Frame(master=self, width=1000, height=12)

        # ----------------------------Cuadro---------------------------

        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        self.cuadro = ttk.Treeview(master=frame_cuadro, columns=("col1", "col2", "col3", "col4"))
        self.cuadro.column("#0")
        self.cuadro.column("col1")
        self.cuadro.column("col2")
        self.cuadro.column("col3")
        self.cuadro.column("col4")

        self.cuadro.heading("#0", text="Producto", anchor='center')
        self.cuadro.heading("col1", text="Codigo", anchor='center')
        self.cuadro.heading("col2", text="Precio", anchor='center')
        self.cuadro.heading("col3", text="Detalle", anchor='center')
        self.cuadro.heading("col4", text="stock", anchor='center')

        self.cuadro.column("#0", width=int(ancho * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(ancho / 10), anchor="center")
        self.cuadro.column("col2", width=int(ancho / 10), anchor="center")
        self.cuadro.column("col3", width=int(ancho * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(ancho / 10), anchor="center")

        # ---------------------scrollbar-------------------
        scrollbar = ttk.Scrollbar(frame_cuadro, orient="vertical", command=self.cuadro.yview)
        scrollbar.pack(side="right", fill="y")

        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        # ----------------------------Ejecutar al abrir---------------------------

        project_functions.pasar_al_cuadro(self.producto, self.cuadro)

        # -----------------------------------------------gestion de eventos----------------------------------------

        self.bind("<Configure>", self.on_resize)
        self.cuadro.configure(yscrollcommand=scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------

        label_alerta.pack()
        sub_label_alerta.pack()
        label_msg.grid(row=0, column=1, pady=6)
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i + 1, column=0)
        for i in range(len(self.entrys)):
            self.entrys[i].grid(row=i + 1, column=1, pady=6)
        button_add.grid(row=3, column=2, padx=20)
        button_new.grid(row=4, column=2, padx=20)
        input_frame.pack()
        buttons_frame.pack(pady=15)
        sub_label_2.pack()
        self.cuadro.pack_configure(fill='x')
        self.update()
        frame_cuadro.place(relx=0.5, y=sub_label_2.winfo_y() + sub_label_2.winfo_reqheight() + 5, relwidth=0.8,
                           height=75, anchor='n')
        button_cancel.place(relx=0.5, rely=0.99, height=40, width=200, anchor='s')


class VentanaEditInfo(ttk.Toplevel):

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

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.actual_focus = 0
        # ----------------------------------------- ventana ---------------------------------------------
        resolution = project_functions.calcular_res_ventana()
        self.parent.withdraw()
        self.title(f'{self.parent.title()} - Editar info productos')
        self.protocol("WM_DELETE_WINDOW", lambda: self.parent.destroy())
        self.geometry(resolution[0])
        self.state('zoomed')
        self.iconbitmap(parent.icon_path)
        # -----------------------------------------------frames---------------------------------------------------
        frame = ttk.Frame(master=self)
        sub_frame = ttk.Frame(master=frame)

        # -----------------------------------------ttk_variables------------------------------------------------
        self.str_buscado = ttk.StringVar()
        self.lost_focus = ttk.BooleanVar()
        self.order_mode = ttk.IntVar()
        # -----------------------------------------simple_variables------------------------------------------------

        # -----------------------------------------bootstrap widgets------------------------------------------------

        # --------------------------- buttons --------------------------
        menu_button = ttk.Button(master=self, text='Volver al menú',  width=17, style='my.TButton',
                                 command=lambda: project_functions.volver_al_menu(self, self.parent))

        button_theme = ttk.Button(master=self, textvariable=parent.str_modo,  width=17, style='my.TButton',
                                  command=lambda: project_functions.cambiar_modo(
                                      project_functions.obtener_config('tema'), self.parent, parent.str_modo))

        checkbutton = ttk.Checkbutton(master=frame, text="Mostrar en orden alfabético", variable=self.order_mode,
                                      command=self.realizar_busqueda)

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=frame, textvariable=self.str_buscado, width=105)

        # --------------------------- labels ---------------------------
        label_titulo = ttk.Label(master=frame, text='Editar productos', font='Calibri 24 bold')

        # --------------------------- cuadro ---------------------------
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        self.cuadro = ttk.Treeview(master=sub_frame, columns=("col1", "col2", "col3", "col4"))
        self.cuadro.column("#0")
        self.cuadro.column("col1")
        self.cuadro.column("col2")
        self.cuadro.column("col3")
        self.cuadro.column("col4")

        self.cuadro.heading("#0", text="Producto", anchor='center')
        self.cuadro.heading("col1", text="Codigo", anchor='center')
        self.cuadro.heading("col2", text="Precio", anchor='center')
        self.cuadro.heading("col3", text="Detalle", anchor='center')
        self.cuadro.heading("col4", text="stock", anchor='center')

        screen_width = int(resolution[1] * 1.3)
        screen_width = int(screen_width * 0.9)

        self.cuadro.column("#0", width=int(screen_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(screen_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(screen_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(screen_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(screen_width / 10), anchor="center")

        font_per_res = {'1476x830': 18,
                        '1353x761': 18,
                        '1292x807': 17,
                        '1230x692': 16,
                        '1107x692': 16,
                        '1050x590': 15,
                        '984x615': 14,
                        '984x787': 13,
                        '984x738': 13,
                        '984x553': 13,
                        '787x590': 12,
                        '615x461': 10}

        self.cuadro.tag_configure('par', foreground="black", background="white",
                                  font=('Calibri', font_per_res[resolution[0]],))
        self.cuadro.tag_configure('impar', foreground="white", background="grey",
                                  font=('Calibri', font_per_res[resolution[0]],))

        # ------------------------- scroll bar -------------------------
        self.scrollbar = ttk.Scrollbar(sub_frame, orient="vertical", command=self.cuadro.yview)
        self.scrollbar.pack(side="right", fill="y")

        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)
        self.cuadro.bind("<Return>", self.edit_selected)
        self.cuadro.bind("<Double-1>", self.edit_selected)
        self.str_buscado.trace_add('write', lambda *args: self.realizar_busqueda())
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
        label_titulo.pack_configure(pady=10)
        checkbutton.pack_configure(pady=10)
        self.entry.pack_configure(pady=10, fill='x', expand=True)
        self.cuadro.pack_configure(fill='both', expand=True)
        sub_frame.pack_configure(fill='both', expand=True)
        button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')

        # se ejecuta instantáneamente
        project_functions.pasar_al_cuadro(project_functions.get_all(), self.cuadro)
