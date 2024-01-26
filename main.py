import ttkbootstrap as ttk
from tkinter import simpledialog, messagebox
import project_functions
from add_products_window import VentAdd
from search_window import VentanaBuscar
from edit_prices_window import VentanaPrecios
from view_sales_window import VentanaVerVentas


# beta 0.1.0


# ----------------------------------------- Funciones menu ---------------------------------------------


# -----------------------------------------cargar_config-----------------------------------------------

class MainWindowC(ttk.Window):

    def solicit_password(self):

        dialog = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show="*")

        if dialog == "4554":
            VentanaPrecios(self)
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    def __init__(self):
        super().__init__()
        # -----------------------------------------ventana_menu------------------------------------------------
        ver = 'Beta-0.1.0'
        resolution, ancho, alto = project_functions.calcular_res_ventana()
        self.style.theme_use(project_functions.obtener_config('tema'))
        self.title(f'Catalogo-{ver}')
        self.state('zoomed')
        self.geometry(resolution)
        # -----------------------------------------bootstrap widgets------------------------------------------------
        # ---------------------------- frames ---------------------------
        frame_for_buttons = ttk.Frame(master=self)

        # ----------------------------botón tema---------------------------
        self.str_modo = ttk.StringVar()
        self.str_modo.set('Modo claro')
        if project_functions.obtener_config('tema') == 'journal_2':
            self.str_modo.set('Modo oscuro')

        button_theme = ttk.Button(master=self, textvariable=self.str_modo,
                                  command=lambda: project_functions.cambiar_modo(
                                      project_functions.obtener_config('tema'), self, self.str_modo), width=20)

        # ---------------------------botónes ventanas internas-------------------------
        button_search = ttk.Button(master=frame_for_buttons, text='Buscar productos',
                                   command=lambda: VentanaBuscar(self), width=25)

        button_add_product = ttk.Button(master=frame_for_buttons, text='Añadir nuevos productos',
                                        command=lambda: VentAdd(self), width=25)

        button_edit_prices = ttk.Button(master=frame_for_buttons, text='Actualizar los precios',
                                        command=self.solicit_password, width=25)

        button_view_sales = ttk.Button(master=frame_for_buttons, text='Listado de ventas',
                                       command=lambda: VentanaVerVentas(self), width=25)

        # ---------------------------label versión-------------------------
        version_label = ttk.Label(master=self, text=f'version: {ver}')

        # ---------------------------------------------- placing widgets -----------------------------------------------
        button_search.pack(pady=15, ipady=3)
        button_add_product.pack(pady=15, ipady=3)
        button_view_sales.pack(pady=15, ipady=3)
        button_edit_prices.pack(pady=15, ipady=3)
        button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')
        frame_for_buttons.place(relx=0.5, rely=0.3, anchor='center')
        version_label.place(relx=0.009, rely=0.99, anchor='sw')
