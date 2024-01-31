import ttkbootstrap as ttk
from tkinter import simpledialog, messagebox
import project_functions
from add_products_window import VentAdd
from search_window import VentanaBuscar
from edit_prices_window import VentanaPrecios
from view_sales_window import VentanaVerVentas
from add_stock_window import VentanaStock
from edit_product_info_window import VentanaEditInfo

# beta 0.1.1


# ----------------------------------------- Funciones menu ---------------------------------------------


# -----------------------------------------cargar_config-----------------------------------------------

class MainWindowC(ttk.Window):

    def solicit_password(self, mode):
        correct_password_introduced = False

        while not correct_password_introduced:
            dialog = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show="*")

            if dialog is None:
                break
            elif dialog == self.password:
                if mode == 0:
                    VentanaPrecios(self)
                elif mode == 1:
                    VentanaEditInfo(self)
                correct_password_introduced = True
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")

    def __init__(self):
        super().__init__()

        # -----------------------------------------variables principales------------------------------------------------
        self.password = '777fer'
        self.icon_path = project_functions.encontrar_ruta_icono()
        # -----------------------------------------ventana_menu------------------------------------------------
        ver = 'Beta-0.1.1'
        resolution, ancho, alto = project_functions.calcular_res_ventana()
        self.style.theme_use(project_functions.obtener_config('tema'))
        self.title(f'Catalogo-{ver}')
        self.state('zoomed')
        self.iconbitmap(self.icon_path)
        self.geometry(resolution)
        # -----------------------------------------bootstrap widgets------------------------------------------------
        # ---------------------------- frames ---------------------------
        frame_for_buttons = ttk.Frame(master=self)

        # ---------------------------- estilos ---------------------------
        menu_button_style = ttk.Style()
        menu_button_style.configure('my.TButton', font='arial 12 bold')
        danger_button_style = ttk.Style()
        danger_button_style.configure('danger.TButton', font='arial 11 bold')
        success_button_style = ttk.Style()
        success_button_style.configure('success.TButton', font='arial 11 bold')
        warning_button_style = ttk.Style()
        warning_button_style.configure('warning.TButton', font='arial 11 bold')
        # ----------------------------botón tema---------------------------
        self.str_modo = ttk.StringVar()
        self.str_modo.set('Modo claro')
        if project_functions.obtener_config('tema') == 'journal_2':
            self.str_modo.set('Modo oscuro')

        button_theme = ttk.Button(master=self, textvariable=self.str_modo,  width=17, style='my.TButton',
                                  command=lambda: project_functions.cambiar_modo(
                                      project_functions.obtener_config('tema'), self, self.str_modo))

        # ---------------------------botónes ventanas internas-------------------------
        button_search = ttk.Button(master=frame_for_buttons, text='Buscar productos',
                                   command=lambda: VentanaBuscar(self), width=23, style='my.TButton')

        button_add_product = ttk.Button(master=frame_for_buttons, text='Añadir nuevos productos',
                                        command=lambda: VentAdd(self), width=23, style='my.TButton')

        button_edit_prices = ttk.Button(master=frame_for_buttons, text='Actualizar los precios',
                                        command=lambda: self.solicit_password(0), width=23, style='my.TButton')

        button_view_sales = ttk.Button(master=frame_for_buttons, text='Listado de ventas',
                                       command=lambda: VentanaVerVentas(self), width=23, style='my.TButton')

        button_add_stock = ttk.Button(master=frame_for_buttons, text='Añadir Stock',
                                      command=lambda: VentanaStock(self), width=23, style='my.TButton')

        button_edit_info = ttk.Button(master=frame_for_buttons, text='Editar productos',
                                      command=lambda: self.solicit_password(1), width=23, style='my.TButton')

        # ---------------------------label versión-------------------------
        version_label = ttk.Label(master=self, text=f'version: {ver}')

        # ---------------------------------------------- placing widgets -----------------------------------------------
        button_search.pack(pady=15, ipady=3)
        button_add_product.pack(pady=15, ipady=3)
        button_view_sales.pack(pady=15, ipady=3)
        button_add_stock.pack(pady=15, ipady=3)
        button_edit_prices.pack(pady=15, ipady=3)
        button_edit_info.pack(pady=15, ipady=3)
        button_theme.place(relx=0.990, y=15, height=40, anchor='ne')
        frame_for_buttons.place(relx=0.5, y=15, anchor='n')
        version_label.place(relx=0.009, rely=0.99, anchor='sw')
