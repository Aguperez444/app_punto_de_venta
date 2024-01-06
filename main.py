import ttkbootstrap as ttk
import project_functions
from search_window import abrir_ventana_buscar

# alpha 0.0.5

# ----------------------------------------- Funciones menu ---------------------------------------------


# -----------------------------------------cargar_config-----------------------------------------------


# -----------------------------------------ventana_menu------------------------------------------------
resolucion, ancho, alto = project_functions.calcular_res_ventana()
main_window = ttk.Window(themename=project_functions.obtener_config('tema'))
main_window.title('Catalogo-Alpha-0.0.4')
main_window.geometry(resolucion)
# -----------------------------------------bootstrap widgets------------------------------------------------
# ----------------------------botón tema---------------------------
str_modo = ttk.StringVar()
str_modo.set('Modo claro')
if project_functions.obtener_config('tema') == 'journal_mod':
    str_modo.set('Modo oscuro')

boton_tema = ttk.Button(master=main_window, textvariable=str_modo,
                        command=lambda: project_functions.cambiar_modo(project_functions.obtener_config('tema'), main_window, str_modo))

# ---------------------------botón buscar-------------------------
button_search = ttk.Button(master=main_window, text='Buscar productos', command=
                            lambda: abrir_ventana_buscar(main_window, str_modo))

# -----------------------------------------------packing---------------------------------------------------
button_search.place(relx = 0.5, rely = 0.1, anchor='center')
boton_tema.place(relx= 0.990, rely= 0.017, anchor='ne')

# -----------------------------------------------Main loop---------------------------------------------------
main_window.after(0, lambda : main_window.state('zoomed'))
main_window.mainloop()
