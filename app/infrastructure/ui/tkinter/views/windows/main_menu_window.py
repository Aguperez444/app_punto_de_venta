import ttkbootstrap as ttk

from tkrouter import StyledRoutedView, RouteLinkButton, create_router, get_router
from app.infrastructure.ui.tkinter.custom_widgets.customRouter import RouterOutlet

from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import BaseProjectWindow

from app.infrastructure.ui.tkinter.views.views.show_products_view import ShowProductsView
from app.infrastructure.ui.tkinter.views.views.add_product_view import AddProductsView
from app.infrastructure.ui.tkinter.views.views.edit_prices_view import EditPricesView
from app.infrastructure.ui.tkinter.views.views.show_sales_list_view import ShowSalesListView
from app.infrastructure.ui.tkinter.views.views.add_stock_view import AddStockView
from app.infrastructure.ui.tkinter.views.views.edit_product_info_view import EditProductInfoView
from app.infrastructure.ui.tkinter.views.views.show_no_stock_list_view import ShowNoStockView


class MainMenuRoutedView(StyledRoutedView):
    def __init__(self, master: RouterOutlet):
        super().__init__(master)
        # -----------------------------------------comunicación con Controllers--------------------------------

        self.parent: 'MainMenuWindow' = master.parent

        # -----------------------------------------bootstrap widgets----------------------------------------------
        self.button_theme = ttk.Button(master=self, textvariable=self.parent.str_modo, width=17, style='my.TButton',
                                       command=self.parent.cambiar_modo)

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

        self.button_search = RouteLinkButton(master=self.frame_for_buttons, to='/showProducts', text='Buscar productos',
                                             width=23, style='my.TButton')

        self.button_add_product = RouteLinkButton(master=self.frame_for_buttons, to='/addProducts',
                                                  text='Añadir nuevos productos', width=23, style='my.TButton')

        self.button_edit_prices = ttk.Button(master=self.frame_for_buttons, text='Actualizar los precios',
                                             command=lambda: self.parent.solicit_password(0), width=23,
                                             style='my.TButton')

        self.button_view_sales = RouteLinkButton(master=self.frame_for_buttons, to='/showSalesList',
                                                 text='Listado de ventas', width=23, style='my.TButton')

        self.button_add_stock = RouteLinkButton(master=self.frame_for_buttons, to='/addStock', text='Añadir Stock',
                                           width=23, style='my.TButton')

        self.button_edit_info = ttk.Button(master=self.frame_for_buttons, text='Editar productos',
                                           command=lambda: self.parent.solicit_password(1), width=23,
                                           style='my.TButton')

        self.button_no_stock = RouteLinkButton(master=self.frame_for_buttons, to='/showNoStockList',
                                               text='Productos sin stock', width=23, style='my.TButton')

        self.button_theme.place(relx=0.990, y=15, height=40, anchor='ne')

        # ---------------------------label versión-------------------------
        self.version_label = ttk.Label(master=self, text=f'version: {self.parent.version}')

        # ---------------------------------------------- placing widgets -----------------------------------------------
        self.frame_for_buttons.place(relx=0.5, y=15, anchor='n')
        self.version_label.place(relx=0.009, rely=0.99, anchor='sw')

        self.button_search.pack(pady=15, ipady=3)
        self.button_add_product.pack(pady=15, ipady=3)
        self.button_edit_prices.pack(pady=15, ipady=3)
        self.button_view_sales.pack(pady=15, ipady=3)
        self.button_add_stock.pack(pady=15, ipady=3)
        self.button_edit_info.pack(pady=15, ipady=3)
        self.button_no_stock.pack(pady=15, ipady=3)


class MainMenuWindow(BaseProjectWindow):
    def __init__(self):
        super().__init__()

        self.minsize(800, 600)

        self.controllerMW = None  # TODO: implementar controller para esta ventana

        self.ROUTES = {
        "/": MainMenuRoutedView,
        "/showProducts": ShowProductsView,
        "/addProducts": AddProductsView,
        "/editPrices": EditPricesView,
        "/showSalesList": ShowSalesListView,
        "/addStock": AddStockView,
        "/editProductInfo": EditProductInfoView,
        "/showNoStockList": ShowNoStockView,
        }


        self.outlet = RouterOutlet(self)
        self.outlet.pack(fill="both", expand=True)

        create_router(self.ROUTES, self.outlet)
        get_router().navigate("/")

        # -----------------------------------------variables principales----------------------------------------
        self.password = '777fer'
        # -----------------------------------------ventana_menu-------------------------------------------------
        self.title(f'Catalogo-{self.version}')
        self.maximizar()

        # ---------------------------------------------- placing widgets -----------------------------------------------


    def handle_correct_password(self, mode: int):
        if mode == 0:
            get_router().navigate("/editPrices")
        elif mode == 1:
            get_router().navigate("/editProductInfo")


