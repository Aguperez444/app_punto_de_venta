import ttkbootstrap as ttk
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.domain.models.producto import Producto


class IHasTable(ABC):

    @property
    @abstractmethod
    def table(self) -> 'SearchTable':
        """Cada clase concreta debe exponer un atributo 'table'"""
        pass

    @abstractmethod
    def table_action(self, event):
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
    def pasar_al_cuadro(self, product_list: list['Producto']):
        self.table.show_products(product_list)
    def clean_treeview(self):
        self.table.clear_all()


class SearchTable(ttk.Frame):
    def __init__(self, parent: ttk.Frame|IHasTable, resolution_str: str, resolution: tuple, title: str,
                 font_param: str = 'Calibri 24 bold'):

        super().__init__(parent)
        self.parent = parent
        self.resolution_str = resolution_str
        self.resolution = resolution
        # --------------------------- frames --------------------------
        self.cuadro_frame = ttk.Frame(master=self)

        # ------------------------ ttk_variables ----------------------
        self.str_buscado = ttk.StringVar()
        self.alfabetico_checked = ttk.IntVar()

        # --------------------------- entry's --------------------------
        self.entry = ttk.Entry(master=self, textvariable=self.str_buscado, width=105)

        # ---------------------------- Buttons ---------------------------

        self.alphabetic_check_button = ttk.Checkbutton(self, text="Mostrar en orden alfabético",
                                                       variable=self.alfabetico_checked,
                                                       command=self.toggle_alphabetic)

        # --------------------------- labels ---------------------------
        self.label_titulo = ttk.Label(master=self, text=title, font=font_param)

        # --------------------------- Cuadro ---------------------------
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)
        self.cuadro = ttk.Treeview(master=self, columns=("col1", "col2", "col3", "col4"))
        self.cuadro.column("#0")
        self.cuadro.column("col1")
        self.cuadro.column("col2")
        self.cuadro.column("col3")
        self.cuadro.column("col4")

        self.cuadro.heading("#0", text="Producto", anchor='center')
        self.cuadro.heading("col1", text="Codigo", anchor='center')
        self.cuadro.heading("col2", text="Precio", anchor='center')
        self.cuadro.heading("col3", text="Detalle", anchor='center')
        self.cuadro.heading("col4", text="stock", anchor='center')

        screen_width = int(self.resolution[1] * 1.3)
        screen_width = int(screen_width * 0.9)

        self.cuadro.column("#0", width=int(screen_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(screen_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(screen_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(screen_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(screen_width / 10), anchor="center")

        font_per_res = {'1476x830': 18,
                        '1353x761': 18,
                        '1292x807': 17,
                        '1230x692': 16,
                        '1107x692': 16,
                        '1050x590': 15,
                        '984x615': 14,
                        '984x787': 13,
                        '984x738': 13,
                        '984x553': 13,
                        '787x590': 12,
                        '615x461': 10
                        }

        self.cuadro.tag_configure('par', foreground="black", background="white",
                                  font=('Calibri', font_per_res[self.resolution_str]))
        self.cuadro.tag_configure('impar', foreground="white", background="grey",
                                  font=('Calibri', font_per_res[self.resolution_str]))

        # ------------------------- scroll bar -------------------------
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.cuadro.yview)


        style_scroll = ttk.Style()
        style_scroll.configure("Vertical.TScrollbar", troughcolor="white")

        # -----------------------------------------------gestion de eventos----------------------------------------
        self.cuadro.configure(yscrollcommand=self.scrollbar.set)

        self.cuadro.bind("<Return>", self.parent.table_action)
        self.cuadro.bind("<Double-1>", self.parent.table_action)
        self.str_buscado.trace_add('write', self.parent.entry_action)

        self.grab_focus()

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
        self.label_titulo.pack_configure(pady=10)

        self.alphabetic_check_button.pack_configure(pady=10)
        self.entry.pack_configure(pady=10, fill='x', expand=True)

        self.scrollbar.pack(side="right", fill="y")
        self.cuadro.pack_configure(fill='both', expand=True)

    def render_no_alphabetic(self):
        self.label_titulo.pack_configure(pady=10)

        self.entry.pack_configure(pady=10, fill='x', expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.cuadro.pack_configure(fill='both', expand=True)

    def render_only_table(self):
        self.label_titulo.pack_configure(pady=10)

        self.scrollbar.pack(side="right", fill="y")
        self.cuadro.pack_configure(fill='both', expand=True)

    def show_products(self, product_list: list['Producto']):
        # Borrar todas las filas existentes en el Treeview
        self.cuadro.delete(*self.cuadro.get_children())
        contador = 0
        # Añadir nuevas filas
        for product in product_list:
            tag = 'par' if contador % 2 == 0 else 'impar'
            self.cuadro.insert("", "end", iid=str(product.id_producto), text=product.nombre, values=(product.codigo,
                                                                          f'{product.precio}', product.detalle,
                                                                          product.stock, product.id_producto),
                               tags=tag)
            contador += 1
        return


    def clear_all(self):
        self.cuadro.delete(*self.cuadro.get_children())


    def adjust_size(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")


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
            if selection[0] == children[0]:
                self.cuadro.selection_clear()
                self.cuadro.focus('')
                self.entry.focus_set()

