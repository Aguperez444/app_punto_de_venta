import ttkbootstrap as ttk
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from app.domain.models.producto import Producto




class IHasTable(ABC):

    @property
    @abstractmethod
    def table(self) -> 'SearchTable':
        """Cada clase concreta debe exponer un atributo 'table'"""
        pass
    @abstractmethod
    def table_action(self, event: Any):
        pass
    @abstractmethod
    def entry_action(self, *args):
        pass
    @abstractmethod
    def search_action(self):
        pass
    @abstractmethod
    def alphabetical_search_action(self):
        pass
    def pasar_al_cuadro(self, product_list: list['Producto']) -> None:
        self.table.show_products(product_list)
    def clean_treeview(self) -> None:
        self.table.clear_all()


class MixinTableNavigation(ABC):
    """PARA USAR ESTE MIXIN DEBE IMPLEMENTAR LA TABLA SI O SI"""
    @property
    @abstractmethod
    def table(self) -> 'SearchTable':
        """Cada clase concreta debe exponer un atributo 'table'"""
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._up_last_time = 0.0
        self._up_count = 0
        self._up_double_threshold = 0.3

    def _on_up_press(self, _event=None) -> None:
        import time
        now = time.monotonic()
        if now - self._up_last_time <= self._up_double_threshold:
            self._up_count += 1
        else:
            self._up_count = 1
        self._up_last_time = now
        if self._up_count >= 2:
            # doble pulsación detectada
            self.change_focus_up(_event)
            self._up_count = 0

    def change_focus_down(self, _event=None) -> None:
        self.table.grab_focus_cuadro()

    def change_focus_up(self, _event=None) -> None:
        self.table.grab_focus_cuadro(going_up=True)


class SearchTable(ttk.Frame):
    def __init__(self, parent: ttk.Frame|IHasTable, resolution_str: str, resolution: tuple, title: str,
                 font_param: str = 'Calibri 24 bold', debounce_ms: int = 250):

        super().__init__(parent)
        self.parent = parent
        self.resolution_str = resolution_str
        self.resolution = resolution
        self._debounce_ms = debounce_ms
        self._search_after_id: str | None = None
        # --------------------------- frames --------------------------
        self.cuadro_frame = ttk.Frame(master=self)

        # ------------------------ ttk_variables ----------------------
        self.str_buscado = ttk.StringVar()
        self.alfabetico_checked = ttk.IntVar()
        self.results_count_var = ttk.StringVar(value="")

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=self, textvariable=self.str_buscado, width=105)

        # ---------------------------- Buttons ---------------------------

        self.alphabetic_check_button = ttk.Checkbutton(self, text="Mostrar en orden alfabético",
                                                       variable=self.alfabetico_checked,
                                                       command=self.toggle_alphabetic)

        # --------------------------- labels ---------------------------
        self.label_titulo = ttk.Label(master=self, text=title, font=font_param)
        self.label_results_count = ttk.Label(
            master=self, textvariable=self.results_count_var, font=('Calibri', 10, 'italic')
        )

        # --------------------------- Cuadro ---------------------------
        self._current_font_size = 14
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        self.cuadro = ttk.Treeview(master=self, columns=("col1", "col2", "col3", "col4"))
        self.cuadro.heading("#0", text="Producto", anchor='w')
        self.cuadro.heading("col1", text="Código", anchor='center')
        self.cuadro.heading("col2", text="Precio", anchor='e')
        self.cuadro.heading("col3", text="Detalle", anchor='w')
        self.cuadro.heading("col4", text="Stock", anchor='center')

        initial_width = max(int(self.resolution[0] * 0.85), 760) if self.resolution else 900
        self._apply_responsive_layout(initial_width)

        # ------------------------- scroll bar -------------------------
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.cuadro.yview)


        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        self.cuadro.bind("<Configure>", self._on_table_configure)
        self.cuadro.bind("<Return>", self.parent.table_action)
        self.cuadro.bind("<Double-1>", self.parent.table_action)
        self.str_buscado.trace_add('write', self._schedule_debounced_search)
        self.bind("<Destroy>", self._cancel_pending_search)


        self.grab_focus()

    def _apply_responsive_layout(self, table_width: int) -> None:
        usable = max(int(table_width) - 22, 560)

        if usable < 860:
            font_size = 11
            rowheight = 26
        elif usable < 1120:
            font_size = 13
            rowheight = 28
        elif usable < 1420:
            font_size = 15
            rowheight = 30
        else:
            font_size = 16
            rowheight = 32

        if font_size != self._current_font_size or not self.cuadro.tag_configure('par', 'font'):
            self._current_font_size = font_size
            ttk.Style().configure('Treeview', rowheight=rowheight)
            self.cuadro.tag_configure(
                'par', foreground="black", background="white", font=('Calibri', font_size)
            )
            self.cuadro.tag_configure(
                'impar', foreground="white", background="grey", font=('Calibri', font_size)
            )
            self.cuadro.tag_configure(
                'inactivo',
                foreground="#666666",
                background="#e6e6e6",
                font=('Calibri', font_size, 'italic'),
            )

        self.cuadro.column("#0", width=int(usable * 0.31), minwidth=150, anchor="w", stretch=True)
        self.cuadro.column("col1", width=int(usable * 0.12), minwidth=80, anchor="center", stretch=True)
        self.cuadro.column("col2", width=int(usable * 0.16), minwidth=115, anchor="e", stretch=True)
        self.cuadro.column("col3", width=int(usable * 0.31), minwidth=150, anchor="w", stretch=True)
        self.cuadro.column("col4", width=int(usable * 0.10), minwidth=65, anchor="center", stretch=True)

    def _on_table_configure(self, event):
        if event.width > 100:
            self._apply_responsive_layout(event.width)

    def _schedule_debounced_search(self, *args):
        self._cancel_pending_search()
        if self._debounce_ms <= 0:
            self.parent.entry_action(*args)
            return
        self._search_after_id = self.after(
            self._debounce_ms, lambda: self._run_debounced_search(*args)
        )

    def _run_debounced_search(self, *args):
        self._search_after_id = None
        if self.winfo_exists():
            self.parent.entry_action(*args)

    def _cancel_pending_search(self, _event=None):
        if self._search_after_id is not None:
            try:
                self.after_cancel(self._search_after_id)
            except Exception:
                pass
            self._search_after_id = None

    def toggle_alphabetic(self):

        if self.its_alphabetic_checked():  # 1 = marcado
            self.parent.alphabetical_search_action()
        else:  # 0 = no marcado
            self.parent.search_action()


    def its_alphabetic_checked(self):
        return True if int(self.alfabetico_checked.get()) == 1 else False


    def configure_title(self, title: str = None, font: str = None):
        if font is not None:
            self.label_titulo.configure(font=font)
        if title is not None:
            self.label_titulo.configure(text=title)

    def render(self):
        self.label_titulo.pack_configure(pady=8)

        self.alphabetic_check_button.pack_configure(pady=6)
        self.entry.pack_configure(pady=6, fill='x', expand=True)
        self.label_results_count.pack_configure(anchor='e', pady=(0, 4))

        self.scrollbar.pack(side="right", fill="y")
        self.cuadro.pack_configure(fill='both', expand=True)

    def render_no_alphabetic(self):
        self.label_titulo.pack_configure(pady=8)

        self.entry.pack_configure(pady=6, fill='x', expand=True)
        self.label_results_count.pack_configure(anchor='e', pady=(0, 4))
        self.scrollbar.pack(side="right", fill="y")

        self.cuadro.pack_configure(fill='both', expand=True)

    def render_only_table(self):
        self.label_titulo.pack_configure(pady=8)

        self.scrollbar.pack(side="right", fill="y")
        self.cuadro.pack_configure(fill='both', expand=True)

    def show_products(self, product_list: list['Producto']):
        # Borrar todas las filas existentes en el Treeview
        self.cuadro.delete(*self.cuadro.get_children())
        contador = 0
        # Añadir nuevas filas
        for product in product_list:
            is_active = getattr(product, 'activo', True)
            if not is_active:
                tag = 'inactivo'
                display_name = f"{product.nombre} [ARCHIVADO]"
            else:
                tag = 'par' if contador % 2 == 0 else 'impar'
                display_name = product.nombre
            self.cuadro.insert("", "end", iid=str(product.id_producto), text=display_name, values=(product.codigo,
                                                                          f'{product.precio}', product.detalle,
                                                                          product.stock, product.id_producto),
                               tags=tag)
            contador += 1
        if contador == 0:
            self.results_count_var.set("Sin resultados")
        elif contador == 1:
            self.results_count_var.set("1 producto encontrado")
        else:
            self.results_count_var.set(f"{contador} productos encontrados")
        return


    def clear_all(self):
        self.cuadro.delete(*self.cuadro.get_children())
        self.results_count_var.set("Sin resultados")


    def adjust_size(self, event=None):
        table_w = self.cuadro.winfo_width()
        if table_w > 100:
            self._apply_responsive_layout(table_w)
        elif event is not None and getattr(event, "width", 0) > 100:
            self._apply_responsive_layout(int(event.width * 0.9))


    def get_selected(self) -> tuple:
        return self.cuadro.selection() # obtiene las filas seleccionadas


    def get_item_data(self, item):
        return self.cuadro.item(item, option='values') # Obtiene los valores de la fila


    def get_search(self) -> str:
        return self.str_buscado.get()

    def grab_focus(self):
        self.entry.focus_set()

    def grab_focus_cuadro(self, going_up: bool = False):

        self.cuadro.focus_set()

        children = self.cuadro.get_children()

        if not children:
            self.cuadro.selection_clear()
            self.cuadro.focus('')
            self.entry.focus_set()
            return

        selection = self.cuadro.selection()


        if not going_up:
                selection = self.cuadro.selection()
                if selection == () or selection[0] == children[0]:
                    first = children[0]
                    self.cuadro.selection_set(first)
                    self.cuadro.focus(first)
                    self.cuadro.see(first)
        else:
            if selection and selection[0] == children[0]:
                self.cuadro.selection_clear()
                self.cuadro.focus('')
                self.entry.focus_set()

