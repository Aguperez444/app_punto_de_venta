import ttkbootstrap as ttk
import project_functions
import datetime


def abrir_ventana_buscar(main_window_in, str_modo_in):
    # ----------------------------------------- Funciones ---------------------------------------------
    def realizar_busqueda(*args):
        a = project_functions.busqueda(str_buscado)
        if a:
            project_functions.pasar_al_cuadro(a, cuadro)
        else:
            cuadro.delete(*cuadro.get_children())


    def on_resize(event):
        # Obtener el nuevo ancho de la ventana
        new_width = event.width

        # Redimensionar las columnas del Treeview
        cuadro.column("#0", width=int(new_width * 2 / 7), anchor="center")
        cuadro.column("col1", width=int(new_width / 7), anchor="center")
        cuadro.column("col2", width=int(new_width / 7), anchor="center")
        cuadro.column("col3", width=int(new_width * 2 / 7), anchor="center")


    def obtener_producto_seleccionado(event):
        item = cuadro.selection()
        if item:
            valores = cuadro.item(item, 'values')
            nombre_producto.set(valores[4])

    def obtener_producto_seleccionado_teclado(event):
        item = cuadro.selection()
        if item and (event.keysym in {'Up', 'Down'}):
            valores = cuadro.item(item, 'values')
            nombre_producto.set(valores[4])

    def registrar_venta(event):
        item = cuadro.selection()
        if item and (event.keysym == 'Return' or event.num == 1):
            valores = cuadro.item(item, 'values')
            fecha_hora_actual = datetime.datetime.now()
            formato = "%Y-%m-%d %H:%M:%S"
            fecha_hora_formateada = fecha_hora_actual.strftime(formato)
            print(f"Registrar venta, producto: {valores[4]}, fecha: {fecha_hora_formateada}")
            # Aquí puedes realizar las acciones que desees al presionar Enter

    # ----------------------------------------- ventana ---------------------------------------------
    resolution = project_functions.calcular_res_ventana()

    main_window_in.withdraw()
    search_window = ttk.Toplevel(main_window_in)
    search_window.title(f'{main_window_in.title()} - Busqueda de productos')
    search_window.protocol("WM_DELETE_WINDOW", lambda: main_window_in.destroy())
    search_window.geometry(resolution[0])

    # -----------------------------------------------frames---------------------------------------------------
    frame = ttk.Frame(master=search_window)
    sub_frame = ttk.Frame(master=frame)

    # -----------------------------------------ttk_variables------------------------------------------------
    str_buscado = ttk.StringVar()

    # -----------------------------------------bootstrap widgets------------------------------------------------
    menu_button = ttk.Button(master=search_window, text='Volver al menú', command=
    lambda: project_functions.volver_al_menu(search_window, main_window_in))

    entry = ttk.Entry(master=frame, textvariable=str_buscado, width=105)

    label_titulo = ttk.Label(master=frame, text='Busqueda de productos', font='Calibri 24 bold')

    str_buscado.trace_add('write', realizar_busqueda)

    # Cuadro de busqueda
    style = ttk.Style()
    style.configure('Treeview', rowheight=30)
    cuadro = ttk.Treeview(master=sub_frame, columns=("col1", "col2", "col3","col4"))
    cuadro.column("#0")
    cuadro.column("col1")
    cuadro.column("col2")
    cuadro.column("col3")
    cuadro.column("col4")

    cuadro.heading("#0", text="Producto")
    cuadro.heading("col1", text="Codigo")
    cuadro.heading("col2", text="Precio")
    cuadro.heading("col3", text="Detalle")
    cuadro.heading("col4", text='')
    cuadro.column("col4", width=0, stretch='no')

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
                    '615x461' : 10}

    cuadro.tag_configure('par', foreground="black", background="white", font=('Calibri', font_per_res[resolution[0]],))
    cuadro.tag_configure('impar', foreground="white", background="grey", font=('Calibri', font_per_res[resolution[0]],))

    scrollbar = ttk.Scrollbar(sub_frame, orient="vertical", command=cuadro.yview)
    scrollbar.pack(side="right", fill="y")

    style_scroll = ttk.Style()
    style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

    cuadro.configure(yscrollcommand=scrollbar.set)

    boton_tema = ttk.Button(master=search_window, textvariable=str_modo_in,
                            command=lambda: project_functions.cambiar_modo(project_functions.obtener_config('tema'), main_window_in,
                                                                           str_modo_in))

    # -----------------------------------------------gestion de eventos----------------------------------------
    search_window.after(0, lambda: search_window.state('zoomed'))
    search_window.bind("<Configure>", on_resize)
    cuadro.bind("<ButtonRelease-1>", obtener_producto_seleccionado)
    cuadro.bind("<KeyRelease>", obtener_producto_seleccionado_teclado)
    cuadro.bind("<Return>", registrar_venta)
    cuadro.bind("<Double-1>", registrar_venta)
    # -----------------------------------------------packing---------------------------------------------------
    menu_button.place(x=15, y=15, anchor='nw')
    frame.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.6, anchor="center")

    label_titulo.pack_configure(pady=10)
    entry.pack_configure(pady=10, fill='x', expand= True)
    cuadro.pack_configure(fill='both', expand=True)
    sub_frame.pack_configure(fill='both', expand=True)
    boton_tema.place(relx=0.990, rely=0.017, anchor='ne')
    # -----------------------------------------------eventos---------------------------------------------------

    nombre_producto = ttk.StringVar()

    # Crear una etiqueta para mostrar el nombre del producto seleccionado
    etiqueta_nombre_producto = ttk.Label(search_window, textvariable=nombre_producto)
    etiqueta_nombre_producto.pack()

    return