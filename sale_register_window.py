import ttkbootstrap as ttk
import project_functions


# alpha 0.0.8

# ventana de alerta de error al registrar venta
def abrir_ventana_alerta(parent_window):
    def aceptar():
        alert_window.destroy()
        parent_window.grab_set()
        return

    ancho = int(parent_window.winfo_width() / 1.2)
    alto = int(parent_window.winfo_height() / 2)
    x = (parent_window.winfo_screenwidth() - ancho) // 2
    y = (parent_window.winfo_screenheight() - alto) // 2
    alert_window = ttk.Toplevel(parent_window)
    alert_window.title('Cantidad invalida')
    alert_window.geometry(f'{ancho}x{alto}+{x}+{y}')
    alert_window.focus_set()
    alert_window.grab_set()

    label_alerta = ttk.Label(master=alert_window, text='Cantidad introducida invalida', font='Arial 20 bold')
    sub_label_alerta = ttk.Label(master=alert_window, text='solo se aceptan números enteros como cantidad')
    sub_label_alerta.configure(font='Arial 15 italic')
    button_confirm = ttk.Button(master=alert_window, text='Aceptar', style='success')
    button_confirm.configure(width=15, command=aceptar)
    label_alerta.pack()
    sub_label_alerta.pack()
    button_confirm.pack(pady=20)

    alert_window.mainloop()


# ventana de venta
class VentanaVenta(ttk.Toplevel):
    # --------------------------------- funciones para esta ventana ----------------------------------

    def venta_confirm(self, id_in, amount_in):
        try:
            a = int(amount_in)
            if a <= 0:
                raise ValueError('cero o negativo no es una cantidad valida')
        except ValueError:
            abrir_ventana_alerta(self)
            return
        project_functions.registrar_venta(id_in, amount_in)
        project_functions.actualizar_stock(id_in, int(amount_in) * (-1))
        self.parent.realizar_busqueda()
        self.destroy()

    def venta_cancel(self):
        self.destroy()

    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")

    def __init__(self, parent, product_id):
        super().__init__()

        # ----------------------------------------- ventana ---------------------------------------------
        self.parent = parent
        resolution = project_functions.calcular_res_ventana()
        ancho = int(resolution[1])
        alto = int(resolution[2] / 1.7)
        x = (self.parent.winfo_screenwidth() - ancho) // 2
        y = (self.parent.winfo_screenheight() - alto) // 2
        self.title(f'Registrar venta')
        self.geometry(f'{ancho}x{alto}+{x}+{y}')
        self.grab_set()
        # -------------------------------------obtención de datos ----------------------------------------

        # datos del producto
        producto = project_functions.busqueda_por_id(product_id)

        # -----------------------------------------ttk_variables------------------------------------------------
        self.cantidad_vendida = ttk.StringVar()
        self.cantidad_vendida.set('1')
        title = f'¿Desea registrar una venta de: {producto[0][1]}?'
        # -----------------------------------------bootstrap widgets------------------------------------------------
        label_titulo = ttk.Label(master=self, text=f'{title}')
        label_titulo.configure(font='Calibri 20 bold')

        label_subtitulo = ttk.Label(master=self, text='Info del producto:', font='Calibri 16 bold')

        if resolution[0] == '615x461' and len(title) > 50:
            label_titulo.configure(font='Calibri 15 bold')
            label_subtitulo.configure(font='Calibri 13 bold')

        confirm_button = ttk.Button(master=self, text='Confirmar venta', style='success',
                                    command=lambda: self.venta_confirm(product_id, self.cantidad_vendida.get()))

        cancel_button = ttk.Button(master=self, text='Cancelar venta', style='danger',
                                   command=self.venta_cancel)

        frame_cuadro = ttk.Frame(master=self, width=1000, height=10)

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

        project_functions.pasar_al_cuadro(producto, self.cuadro)

        entry_frame = ttk.Frame(master=self, width=120, height=40)
        label_entry = ttk.Label(master=entry_frame, text='Cantidad:', font='Calibri 14 bold')
        if resolution[0] == '615x461':
            label_entry.configure(font='Calibri 12 bold')
        entry_cantidad_vendida = ttk.Entry(master=entry_frame, textvariable=self.cantidad_vendida, width=3)

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Configure>", self.on_resize)

        # ---------------------------------------------- placing widgets -----------------------------------------------
        label_titulo.pack()
        label_subtitulo.pack()
        self.cuadro.pack_configure(fill='both', expand=True)
        frame_cuadro.place(relx=0.5, rely=0.5, relwidth=0.9, height=63, anchor='center')
        confirm_button.place(relx=0.8, rely=0.8, anchor='center')
        confirm_button.place_configure(width=160, height=60)
        cancel_button.place(relx=0.2, rely=0.8, anchor='center')
        cancel_button.place_configure(width=160, height=60)
        entry_frame.place(relx=0.5, rely=0.3, anchor='center')
        label_entry.place(relx=0, rely=0, anchor='nw')
        entry_cantidad_vendida.place(relx=1, rely=0, anchor='ne')
