import ttkbootstrap as ttk
import project_functions
from add_products_window import VentAdd
from search_window import VentanaBuscar


# alpha 0.0.8

# ----------------------------------------- Funciones menu ---------------------------------------------


# -----------------------------------------cargar_config-----------------------------------------------

class MainWindowC(ttk.Window):
    def __init__(self):
        super().__init__()
        # -----------------------------------------ventana_menu------------------------------------------------
        ver = 'Alpha-0.0.8'
        resolution, ancho, alto = project_functions.calcular_res_ventana()
        self.style.theme_use(project_functions.obtener_config('tema'))
        self.title(f'Catalogo-{ver}')
        self.state('zoomed')
        self.geometry(resolution)
        # -----------------------------------------bootstrap widgets------------------------------------------------
        # ----------------------------botón tema---------------------------
        str_modo = ttk.StringVar()
        str_modo.set('Modo claro')
        if project_functions.obtener_config('tema') == 'journal_mod':
            str_modo.set('Modo oscuro')

        button_theme = ttk.Button(master=self, textvariable=str_modo,
                                  command=lambda: project_functions.cambiar_modo(
                                      project_functions.obtener_config('tema'), self, str_modo))

        # ---------------------------botónes ventanas internas-------------------------
        button_search = ttk.Button(master=self, text='Buscar productos',
                                   command=lambda: VentanaBuscar(self, str_modo))

        button_add_product = ttk.Button(master=self, text='Añadir nuevos productos',
                                        command=lambda: VentAdd(self, str_modo))

        # ---------------------------label versión-------------------------
        version_label = ttk.Label(master=self, text=f'version: {ver}')

        # ---------------------------------------------- placing widgets -----------------------------------------------
        button_search.place(relx=0.5, rely=0.1, anchor='center')
        button_add_product.place(relx=0.5, rely=0.2, anchor='center')
        button_theme.place(relx=0.990, rely=0.017, anchor='ne')
        version_label.place(relx=0.009, rely=0.99, anchor='sw')

        # -----------------------------------------------Main loop------------------------------------------------------


main_window1 = MainWindowC()

main_window1.mainloop()
