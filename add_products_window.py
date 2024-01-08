import ttkbootstrap as ttk
import project_functions


# alpha 0.0.7

def abrir_ventana_alerta(parent_window, success):
    def aceptar(*args):
        alert_window.destroy()
        parent_window.grab_set()
        return

    ancho = int(parent_window.winfo_width() / 4)
    alto = int(parent_window.winfo_height() / 6)
    x = (parent_window.winfo_screenwidth() - ancho) // 2
    y = (parent_window.winfo_screenheight() - alto) // 2
    alert_window = ttk.Toplevel(parent_window)
    alert_window.title('alerta - Error')
    if success:
        alert_window.title('alerta - Producto agregado exitosamente')
    alert_window.geometry(f'{ancho}x{alto}+{x}+{y}')
    alert_window.focus_set()
    alert_window.grab_set()

    label_alerta = ttk.Label(master=alert_window, text='Algo malio sal :(')
    if success:
        label_alerta = ttk.Label(master=alert_window, text='producto agregado exitosamente')
    label_alerta.configure(font='Arial 20 bold')

    button_confirm = ttk.Button(master=alert_window, text='Aceptar', style='success')
    button_confirm.configure(width=15, command=aceptar)
    label_alerta.pack()
    button_confirm.place(relx=0.5, rely=0.8, anchor='center', width=100, height=40)

    alert_window.bind('<Return>', aceptar)

    alert_window.mainloop()


def abrir_ventana_crud(main_window_in, str_modo_in):
    # --------------------------------- funciones para esta ventana ----------------------------------

    def get_data():
        nombre = product_name.get()
        codigo = product_code.get()
        precio = product_price.get()
        detalles = product_details.get()
        codigo_barras = product_bar_code.get()
        stock = product_stock.get()
        vec_datos = [nombre, codigo, precio, detalles, codigo_barras, stock]
        return vec_datos

    def add_product():
        datos_producto = get_data()
        exitoso = project_functions.add_to_db(datos_producto)
        abrir_ventana_alerta(add_p_window, exitoso)

    def nuevo():
        product_name.set('')
        product_code.set('')
        product_price.set('$')
        product_details.set('')
        product_bar_code.set('')
        product_stock.set('1')
    # ----------------------------------------- ventana ---------------------------------------------
    resolution = project_functions.calcular_res_ventana()

    main_window_in.withdraw()
    add_p_window = ttk.Toplevel(main_window_in)
    add_p_window.title(f'{main_window_in.title()} - Busqueda de productos')
    add_p_window.protocol("WM_DELETE_WINDOW", lambda: main_window_in.destroy())
    add_p_window.geometry(resolution[0])
    add_p_window.state('zoomed')

    # -----------------------------------------ttk_variables------------------------------------------------
    product_name = ttk.StringVar()
    product_code = ttk.StringVar()
    product_price = ttk.StringVar(value='$')
    product_details = ttk.StringVar()
    product_bar_code = ttk.StringVar()
    product_stock = ttk.StringVar(value='1')

    # -----------------------------------------bootstrap widgets------------------------------------------------

    # ----------------------------frames---------------------------
    input_frame = ttk.Frame(master=add_p_window)

    # ----------------------------entry's---------------------------
    product_name_entry = ttk.Entry(master=input_frame, textvariable=product_name, width=30)
    product_code_entry = ttk.Entry(master=input_frame, textvariable=product_code, width=30)
    product_price_entry = ttk.Entry(master=input_frame, textvariable=product_price, width=30)
    product_details_entry = ttk.Entry(master=input_frame, textvariable=product_details, width=30)
    product_bar_code_entry = ttk.Entry(master=input_frame, textvariable=product_bar_code, width=30)
    product_stock_entry = ttk.Entry(master=input_frame, textvariable=product_stock, width=30)

    # ----------------------------labels---------------------------
    label_name = ttk.Label(master=input_frame, text='                     Nombre:', anchor='e', font='arial 13')
    label_code = ttk.Label(master=input_frame, text='                     Codigo:', anchor='e', font='arial 13')
    label_price = ttk.Label(master=input_frame, text='                     Precio:', anchor='e', font='arial 13')
    label_details = ttk.Label(master=input_frame, text='                    Detalle:', anchor='e', font='arial 13')
    label_bar_code = ttk.Label(master=input_frame, text='      Codigo de barras:', anchor='e', font='arial 13')
    label_stock = ttk.Label(master=input_frame, text='                      Stock:', anchor='e', font='arial 13')
    label_msg = ttk.Label(master=input_frame, text='Ingrese los datos del producto', font='Arial 14 bold')

    # ----------------------------buttons---------------------------
    boton_tema = ttk.Button(master=add_p_window, textvariable=str_modo_in,
                            command=lambda: project_functions.cambiar_modo(project_functions.obtener_config('tema'),
                                                                           main_window_in, str_modo_in))

    button_add = ttk.Button(master=input_frame, text='Agregar producto', width=18, style='success', command=add_product)

    button_new = ttk.Button(master=input_frame, text='Nuevo', width=18, style='warning', command=nuevo)

    menu_button = ttk.Button(master=add_p_window, text='Volver al menú',
                             command=lambda: project_functions.volver_al_menu(add_p_window, main_window_in))
    # -----------------------------------------------gestion de eventos----------------------------------------

    # none

    # -----------------------------------------------packing---------------------------------------------------
    boton_tema.place(relx=0.990, rely=0.017, anchor='ne')
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
