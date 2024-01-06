import ttkbootstrap as ttk
import project_functions
import datetime

def abrir_ventana_venta(main_window_in, product_id):
    # --------------------------------- funciones para esta ventana ----------------------------------
    def venta_confirm():
        print('venta confirmada')
        sale_register_window.destroy()

    def venta_cancel():
        print('venta cancelada')
        sale_register_window.destroy()

    def on_resize(event):
        # Obtener el nuevo ancho de la ventana
        new_width = event.width

        # Redimensionar las columnas del Treeview
        cuadro.column("#0", width=int(new_width * 2 / 7), anchor="center")
        cuadro.column("col1", width=int(new_width / 7), anchor="center")
        cuadro.column("col2", width=int(new_width / 7), anchor="center")
        cuadro.column("col3", width=int(new_width * 2 / 7), anchor="center")
    # ----------------------------------------- ventana ---------------------------------------------
    resolution = project_functions.calcular_res_ventana()
    new_res = f'{int(resolution[1])}x{int(resolution[2]/1.7)}'
    sale_register_window = ttk.Toplevel(main_window_in)
    sale_register_window.title(f'Registrar venta')
    sale_register_window.geometry(new_res)
    sale_register_window.grab_set()
    # -------------------------------------obtencion de datos ----------------------------------------
    # fecha y hora
    fecha_hora_actual = datetime.datetime.now()
    formato_fecha = "%Y-%m-%d"
    formato_hora = "%H:%M:%S"
    fecha = fecha_hora_actual.strftime(formato_fecha)
    hora = fecha_hora_actual.strftime(formato_hora)

    # datos del producto
    producto = project_functions.busqueda_por_id(product_id)


    # -----------------------------------------ttk_variables------------------------------------------------
    title = f'¿Desea registrar una venta de: {producto[0][1]}?'

    # -----------------------------------------bootstrap widgets------------------------------------------------
    label_titulo = ttk.Label(master=sale_register_window, text=f'{title}')
    label_titulo.configure(font='Calibri 20 bold')

    label_subtitulo = ttk.Label(master=sale_register_window, text='Info del producto:', font='Calibri 14 bold')

    if resolution[0] == '615x461' and len(title) > 50:
        label_titulo.configure(font='Calibri 15 bold')
        label_subtitulo.configure(font='Calibri 12 bold')

    confirm_button = ttk.Button(master=sale_register_window, text='Confirmar venta', style='success', command=venta_confirm)
    cancel_button = ttk.Button(master=sale_register_window, text='Cancelar venta', style='danger', command=venta_cancel)


    frame_cuadro = ttk.Frame(master=sale_register_window ,width=1000, height=10)

    style = ttk.Style()
    style.configure('Treeview', rowheight=30)
    cuadro = ttk.Treeview(master=frame_cuadro, columns=("col1", "col2", "col3"))
    cuadro.column("#0")
    cuadro.column("col1")
    cuadro.column("col2")
    cuadro.column("col3")

    cuadro.heading("#0", text="Producto")
    cuadro.heading("col1", text="Codigo")
    cuadro.heading("col2", text="Precio")
    cuadro.heading("col3", text="Detalle")

    project_functions.pasar_al_cuadro(producto, cuadro)

    # -----------------------------------------------gestion de eventos----------------------------------------
    sale_register_window.bind("<Configure>", on_resize)

    # -----------------------------------------------packing---------------------------------------------------
    label_titulo.pack()
    label_subtitulo.pack()
    cuadro.pack_configure(fill='both', expand=True)
    frame_cuadro.place(relx=0.5, rely=0.3, relwidth=0.9, height=63, anchor='center')
    confirm_button.place(relx=0.8, rely = 0.8, anchor='center')
    confirm_button.place_configure(width=160, height=60)
    cancel_button.place(relx=0.2, rely = 0.8, anchor='center')
    cancel_button.place_configure(width=160, height=60)
