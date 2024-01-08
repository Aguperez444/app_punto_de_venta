import ttkbootstrap as ttk
import project_functions
from search_window import abrir_ventana_buscar
from add_products_window import abrir_ventana_crud

# alpha 0.0.7

# ----------------------------------------- Funciones menu ---------------------------------------------


# -----------------------------------------cargar_config-----------------------------------------------


# -----------------------------------------ventana_menu------------------------------------------------
ver = 'Alpha-0.0.7'
resolucion, ancho, alto = project_functions.calcular_res_ventana()
main_window = ttk.Window(themename=project_functions.obtener_config('tema'))
main_window.title(f'Catalogo-{ver}')
main_window.state('zoomed')
main_window.geometry(resolucion)
# -----------------------------------------bootstrap widgets------------------------------------------------
# ----------------------------botón tema---------------------------
str_modo = ttk.StringVar()
str_modo.set('Modo claro')
if project_functions.obtener_config('tema') == 'journal_mod':
    str_modo.set('Modo oscuro')

boton_tema = ttk.Button(master=main_window, textvariable=str_modo,
                        command=lambda:
                        project_functions.cambiar_modo(project_functions.obtener_config('tema'), main_window, str_modo))

# ---------------------------botónes ventanas internas-------------------------
button_search = ttk.Button(master=main_window, text='Buscar productos',
                           command=lambda: abrir_ventana_buscar(main_window, str_modo))

button_add_product = ttk.Button(master=main_window, text='Añadir nuevos productos',
                                command=lambda: abrir_ventana_crud(main_window, str_modo))

# ---------------------------label versión-------------------------
version_label = ttk.Label(master=main_window, text=f'version: {ver}')

# -----------------------------------------------packing---------------------------------------------------
button_search.place(relx=0.5, rely=0.1, anchor='center')
button_add_product.place(relx=0.5, rely=0.2, anchor='center')
boton_tema.place(relx=0.990, rely=0.017, anchor='ne')
version_label.place(relx=0.009, rely=0.99, anchor='sw')

# -----------------------------------------------Main loop---------------------------------------------------

main_window.mainloop()
