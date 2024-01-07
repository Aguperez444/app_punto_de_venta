import ttkbootstrap as ttk
import project_functions
from sale_register_window import abrir_ventana_venta


# alpha 0.0.6

def abrir_ventana_buscar(main_window_in, str_modo_in):
    # ----------------------------------------- Funciones ---------------------------------------------
    def realizar_busqueda(*args):
        a = project_functions.busqueda(str_buscado)
        if a:
            project_functions.pasar_al_cuadro(a, cuadro)
        else:
            cuadro.delete(*cuadro.get_children())

    def on_focus_out(*args):
        foco_actual = search_window.focus_get()
        if foco_actual != cuadro and foco_actual != entry:
            lost_focus.set(True)

    def on_focus_in(*args):
        if lost_focus.get():
            lost_focus.set(False)
            realizar_busqueda()

    def on_resize(event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        cuadro.column("col1", width=int(new_width / 10), anchor="center")
        cuadro.column("col2", width=int(new_width / 10), anchor="center")
        cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        cuadro.column("col4", width=int(new_width / 10), anchor="center")

    def registrar_venta(event):
        tuple_items = cuadro.selection()
        item = tuple_items[0]
        if item and (event.keysym == 'Return' or event.num == 1):
            valores = cuadro.item(item, option='values')
            product_id = valores[4]
            abrir_ventana_venta(search_window, product_id)

    # ----------------------------------------- ventana ---------------------------------------------
    resolution = project_functions.calcular_res_ventana()

    main_window_in.withdraw()
    search_window = ttk.Toplevel(main_window_in)
    search_window.title(f'{main_window_in.title()} - Busqueda de productos')
    search_window.protocol("WM_DELETE_WINDOW", lambda: main_window_in.destroy())
    search_window.geometry(resolution[0])
    search_window.state('zoomed')
    # -----------------------------------------------frames---------------------------------------------------
    frame = ttk.Frame(master=search_window)
    sub_frame = ttk.Frame(master=frame)

    # -----------------------------------------ttk_variables------------------------------------------------
    str_buscado = ttk.StringVar()
    lost_focus = ttk.BooleanVar()

    # -----------------------------------------bootstrap widgets------------------------------------------------
    menu_button = ttk.Button(master=search_window, text='Volver al menú',
                             command=lambda: project_functions.volver_al_menu(search_window, main_window_in))

    entry = ttk.Entry(master=frame, textvariable=str_buscado, width=105)

    label_titulo = ttk.Label(master=frame, text='Busqueda de productos', font='Calibri 24 bold')

    str_buscado.trace_add('write', realizar_busqueda)

    # Cuadro de busqueda
    style = ttk.Style()
    style.configure('Treeview', rowheight=30)
    cuadro = ttk.Treeview(master=sub_frame, columns=("col1", "col2", "col3", "col4"))
    cuadro.column("#0")
    cuadro.column("col1")
    cuadro.column("col2")
    cuadro.column("col3")
    cuadro.column("col4")

    cuadro.heading("#0", text="Producto", anchor='center')
    cuadro.heading("col1", text="Codigo", anchor='center')
    cuadro.heading("col2", text="Precio", anchor='center')
    cuadro.heading("col3", text="Detalle", anchor='center')
    cuadro.heading("col4", text="stock", anchor='center')

    screen_width = int(resolution[1] * 1.3)
    screen_width = int(screen_width * 0.9)

    cuadro.column("#0", width=int(screen_width * 3 / 10), anchor="center")
    cuadro.column("col1", width=int(screen_width / 10), anchor="center")
    cuadro.column("col2", width=int(screen_width / 10), anchor="center")
    cuadro.column("col3", width=int(screen_width * 3 / 10), anchor="center")
    cuadro.column("col4", width=int(screen_width / 10), anchor="center")

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

    cuadro.tag_configure('par', foreground="black", background="white", font=('Calibri', font_per_res[resolution[0]],))
    cuadro.tag_configure('impar', foreground="white", background="grey", font=('Calibri', font_per_res[resolution[0]],))

    scrollbar = ttk.Scrollbar(sub_frame, orient="vertical", command=cuadro.yview)
    scrollbar.pack(side="right", fill="y")

    style_scroll = ttk.Style()
    style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

    cuadro.configure(yscrollcommand=scrollbar.set)

    boton_tema = ttk.Button(master=search_window, textvariable=str_modo_in,
                            command=lambda: project_functions.cambiar_modo(project_functions.obtener_config('tema'),
                                                                           main_window_in, str_modo_in))

    # -----------------------------------------------gestion de eventos----------------------------------------
    search_window.bind("<Configure>", on_resize)
    search_window.bind("<FocusIn>", on_focus_in)
    search_window.bind("<FocusOut>", on_focus_out)
    cuadro.bind("<Return>", registrar_venta)
    cuadro.bind("<Double-1>", registrar_venta)
    # -----------------------------------------------packing---------------------------------------------------
    menu_button.place(x=15, y=15, anchor='nw')
    frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.6, anchor="center")
    label_titulo.pack_configure(pady=10)
    entry.pack_configure(pady=10, fill='x', expand=True)
    cuadro.pack_configure(fill='both', expand=True)
    sub_frame.pack_configure(fill='both', expand=True)
    boton_tema.place(relx=0.990, rely=0.017, anchor='ne')

    return
