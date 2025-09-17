import ttkbootstrap as ttk

from Views.no_stock_list_window import VentanaNoStock

from Views.base_window_toplevel import BaseProjectWindow

from Controllers.add_product_controller import AddProductController
from Controllers.find_product_controller import FindProductController
from Controllers.add_stock_controller import AddStockController
from Controllers.view_sales_controller import ViewSalesController
from Controllers.edit_prices_controller import EditPricesController
from Controllers.edit_product_info_controller import EditProductInfoController



class MainWindowC(BaseProjectWindow):

    def handle_correct_password(self, mode: int):
        if mode == 0:
            EditPricesController(self)
        elif mode == 1:
            EditProductInfoController(self)


    def __init__(self):
        super().__init__()
        # -----------------------------------------comunicación con Controllers--------------------------------

        self.controllerMW = None  # TODO: implementar controller para esta ventana

        # -----------------------------------------variables principales----------------------------------------
        self.password = '777fer'
        # -----------------------------------------ventana_menu-------------------------------------------------
        self.title(f'Catalogo-{self.version}')
        self.maximizar()

        # -----------------------------------------bootstrap widgets----------------------------------------------
        # ---------------------------- estilos ---------------------------
        menu_button_style = ttk.Style()
        menu_button_style.configure('my.TButton', font='arial 12 bold')
        danger_button_style = ttk.Style()
        danger_button_style.configure('danger.TButton', font='arial 11 bold')
        success_button_style = ttk.Style()
        success_button_style.configure('success.TButton', font='arial 11 bold')
        warning_button_style = ttk.Style()
        warning_button_style.configure('warning.TButton', font='arial 11 bold')

        # ---------------------------- frames ---------------------------
        self.frame_for_buttons = ttk.Frame(master=self)

        # ---------------------------botones ventanas internas-------------------------

        self.button_search = ttk.Button(master=self.frame_for_buttons, text='Buscar productos',
                                        command=lambda: FindProductController(self), width=23, style='my.TButton')

        self.button_add_product = ttk.Button(master=self.frame_for_buttons, text='Añadir nuevos productos',
                                             command=lambda: AddProductController(self), width=23, style='my.TButton')

        self.button_edit_prices = ttk.Button(master=self.frame_for_buttons, text='Actualizar los precios',
                                        command=lambda: self.solicit_password(0), width=23, style='my.TButton')

        self.button_view_sales = ttk.Button(master=self.frame_for_buttons, text='Listado de ventas',
                                       command=lambda: ViewSalesController(self), width=23, style='my.TButton')

        self.button_add_stock = ttk.Button(master=self.frame_for_buttons, text='Añadir Stock',
                                      command=lambda: AddStockController(self), width=23, style='my.TButton')

        self.button_edit_info = ttk.Button(master=self.frame_for_buttons, text='Editar productos',
                                      command=lambda: self.solicit_password(1), width=23, style='my.TButton')

        self.button_no_stock = ttk.Button(master=self.frame_for_buttons, text='Productos sin stock',
                                     command=lambda: VentanaNoStock(self), width=23, style='my.TButton')
        # ---------------------------label versión-------------------------
        self.version_label = ttk.Label(master=self, text=f'version: {self.version}')

        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.button_search.pack(pady=15, ipady=3)
        self.button_add_product.pack(pady=15, ipady=3)
        self.button_view_sales.pack(pady=15, ipady=3)
        self.button_add_stock.pack(pady=15, ipady=3)
        self.button_edit_prices.pack(pady=15, ipady=3)
        self.button_edit_info.pack(pady=15, ipady=3)
        self.button_no_stock.pack(pady=15, ipady=3)
        self.button_theme.place(relx=0.990, y=15, height=40, anchor='ne')
        self.frame_for_buttons.place(relx=0.5, y=15, anchor='n')
        self.version_label.place(relx=0.009, rely=0.99, anchor='sw')
