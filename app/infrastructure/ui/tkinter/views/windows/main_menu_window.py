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
from app.infrastructure.ui.tkinter.views.popups.settings_popup import SettingsPopup


class MainMenuRoutedView(StyledRoutedView):
    def __init__(self, master: RouterOutlet):
        super().__init__(master)
        self.parent: "MainMenuWindow" = master.parent

        self.button_theme = ttk.Button(
            master=self,
            textvariable=self.parent.str_modo,
            width=17,
            style="my.TButton",
            takefocus=False,
            command=self._toggle_theme_and_refresh,
        )

        self._configure_styles()

        self.frame_for_buttons = ttk.Frame(master=self)

        self.button_search = RouteLinkButton(
            master=self.frame_for_buttons,
            to="/showProducts",
            text="Buscar productos",
            width=26,
            style="my.TButton",
        )
        self.button_add_product = RouteLinkButton(
            master=self.frame_for_buttons,
            to="/addProducts",
            text="Añadir nuevos productos",
            width=26,
            style="my.TButton",
        )
        self.button_edit_prices = ttk.Button(
            master=self.frame_for_buttons,
            text="Actualizar los precios",
            command=lambda: self.parent.solicit_password(0),
            width=26,
            style="my.TButton",
        )
        self.button_view_sales = RouteLinkButton(
            master=self.frame_for_buttons,
            to="/showSalesList",
            text="Listado de ventas",
            width=26,
            style="my.TButton",
        )
        self.button_add_stock = RouteLinkButton(
            master=self.frame_for_buttons,
            to="/addStock",
            text="Añadir Stock",
            width=26,
            style="my.TButton",
        )
        self.button_edit_info = ttk.Button(
            master=self.frame_for_buttons,
            text="Editar productos",
            command=lambda: self.parent.solicit_password(1),
            width=26,
            style="my.TButton",
        )
        self.button_no_stock = RouteLinkButton(
            master=self.frame_for_buttons,
            to="/showNoStockList",
            text="Productos sin stock",
            width=26,
            style="my.TButton",
        )

        self._menu_items: list[tuple[ttk.Button, str]] = [
            (self.button_search, "Buscar productos"),
            (self.button_add_product, "Añadir nuevos productos"),
            (self.button_view_sales, "Listado de ventas"),
            (self.button_add_stock, "Añadir Stock"),
            (self.button_no_stock, "Productos sin stock"),
            # Opciones protegidas con contraseña agrupadas al final
            (self.button_edit_prices, "Actualizar los precios"),
            (self.button_edit_info, "Editar productos"),
        ]
        self._selected_index = 0

        self.button_settings = ttk.Button(
            master=self,
            text="Configuración",
            width=17,
            style="my.TButton",
            takefocus=False,
            command=self._open_settings,
        )

        self.button_settings.place(x=15, y=14, anchor="nw")
        self.button_theme.place(relx=0.990, y=14, anchor="ne")

        self.version_label = ttk.Label(master=self, text=f"version: {self.parent.version}")
        self.nav_hint_label = ttk.Label(
            master=self,
            text="Use ↑ / ↓ para moverse y Enter para abrir la opción seleccionada",
            font="Arial 10 italic",
        )

        self.frame_for_buttons.place(relx=0.5, y=18, anchor="n")
        self.version_label.place(relx=0.009, rely=0.99, anchor="sw")
        self.nav_hint_label.place(relx=0.5, rely=0.97, anchor="s")

        for idx, (btn, _label) in enumerate(self._menu_items):
            btn.configure(takefocus=False)
            btn.pack(pady=13, ipady=3)
            btn.bind("<Enter>", lambda _e, i=idx: self._select_index(i))

        self._apply_selection_highlight()

        self.parent.bind("<Up>", self._on_nav_up)
        self.parent.bind("<Down>", self._on_nav_down)
        self.parent.bind("<Return>", self._on_nav_enter)
        self.parent.bind("<KP_Enter>", self._on_nav_enter)
        self.bind("<Destroy>", self._cleanup_bindings)
        self.after_idle(self._focus_menu)

    def _open_settings(self) -> None:
        SettingsPopup(self.parent)
        self.after_idle(self._focus_menu)

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.configure("my.TButton", font="arial 12 bold")
        style.configure("danger.TButton", font="arial 11 bold")
        style.configure("success.TButton", font="arial 12 bold")
        style.configure("warning.TButton", font="arial 11 bold")
        style.configure("info.TButton", font="arial 12 bold")

    def _toggle_theme_and_refresh(self) -> None:
        self.parent.cambiar_modo()
        self._configure_styles()
        self._apply_selection_highlight()
        self._focus_menu()

    def _focus_menu(self) -> None:
        if self.winfo_exists():
            self.focus_set()

    def _is_main_window_active(self) -> bool:
        if not self.winfo_exists():
            return False
        focused = self.parent.focus_get()
        if focused is not None and focused.winfo_toplevel() != self.parent:
            return False
        return True

    def _select_index(self, index: int) -> None:
        self._selected_index = index % len(self._menu_items)
        self._apply_selection_highlight()

    def _apply_selection_highlight(self) -> None:
        for idx, (btn, label) in enumerate(self._menu_items):
            if idx == self._selected_index:
                btn.configure(style="success.TButton", text=f"▶  {label}  ◀")
            else:
                btn.configure(style="my.TButton", text=label)

    def _on_nav_up(self, _event=None):
        if not self._is_main_window_active():
            return None
        self._select_index(self._selected_index - 1)
        return "break"

    def _on_nav_down(self, _event=None):
        if not self._is_main_window_active():
            return None
        self._select_index(self._selected_index + 1)
        return "break"

    def _on_nav_enter(self, _event=None):
        if not self._is_main_window_active():
            return None
        btn, _ = self._menu_items[self._selected_index]
        btn.invoke()
        return "break"

    def _cleanup_bindings(self, event=None) -> None:
        if event is not None and event.widget is not self:
            return
        try:
            self.parent.unbind("<Up>")
            self.parent.unbind("<Down>")
            self.parent.unbind("<Return>")
            self.parent.unbind("<KP_Enter>")
        except Exception:
            pass


class MainMenuWindow(BaseProjectWindow):
    def __init__(self, container=None):
        super().__init__(container=container)

        self.minsize(800, 600)

        self.controllerMW = None

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

        self.title(f"Catalogo-{self.version}")
        self.maximizar()

    def handle_correct_password(self, mode: int):
        if mode == 0:
            get_router().navigate("/editPrices")
        elif mode == 1:
            get_router().navigate("/editProductInfo")
