import ttkbootstrap as ttk
from tkinter import simpledialog, messagebox, PhotoImage
from Controllers.common_window_innit_controller import CommonWindowInitController #TODO CHECKEAR ORDEN DE INSTANCIAMIENTO DE CONTROLLERS
from PIL import Image, ImageTk
from tkinter import TclError

from Models.producto import Producto



class BaseProjectWindow(ttk.Window):
    """
    Base class for project windows, providing common functionality.
    """
    def __init__(self):
        super().__init__()
        self.password = '777fer'  # Default password, can be overridden in subclasses
        # -----------------------------------------comunicación con Controllers--------------------------------
        self.init_controller = CommonWindowInitController()
        # -----------------------------------------atributos principales----------------------------------------
        self.icon_path = self.init_controller.get_icon_path() # obtain the path to the icon
        self.version = self.init_controller.get_version() # obtain the program version
        self.geometry = self.init_controller.calculate_window_resolution() # calculate the window resolution
        self.img = Image.open(self.icon_path)
        self.icon: PhotoImage = ImageTk.PhotoImage(self.img)
        self.theme = self.init_controller.obtener_tema_actual()

        self.minsize(400, 300)

        #self.iconbitmap(self.icon_path) funcionaba en windows no en linux
        self.wm_iconphoto(False, self.icon) #marca en naranja pero funciona bien

        self.style.theme_use(self.theme)


        # ----------------------------botón tema---------------------------
        self.str_modo = ttk.StringVar()
        self.str_modo.set('Modo claro')
        if self.theme == 'journal':
            self.str_modo.set('Modo oscuro')

        self.button_theme = ttk.Button(master=self, textvariable=self.str_modo, width=17, style='my.TButton',
                                       command=self.cambiar_modo)


    def solicit_password(self, mode):
        correct_password_introduced = False

        while not correct_password_introduced:
            dialog = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show="*")

            if dialog is None:
                break
            elif dialog == self.password:
                self.handle_correct_password(mode)
                correct_password_introduced = True
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")


    def handle_correct_password(self, mode):
        """
        Handle the action to take when the correct password is entered.
        To be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")


    def cambiar_modo(self):
        if self.theme == 'journal':
            self.style.theme_use('darkly')
            self.theme = 'darkly'
            self.str_modo.set('Modo claro')


        else:
            self.style.theme_use('journal')
            self.theme = 'journal'
            self.str_modo.set('Modo oscuro')

        self.init_controller.tema_cambiado(self.theme)


    def cerrar_ventana_alerta(self):
        raise NotImplementedError("Subclasses should implement this method.")


    @staticmethod
    def show_error(msg):
        messagebox.showerror('Ha ocurrido un error', msg)


    def maximizar(self):
        try:
            self.attributes('-zoomed', True)
        except TclError:
            self.state('zoomed')


class BaseProjectWindowToplevel(ttk.Toplevel):
    """
    Base class for project topLevel windows, providing common functionality.
    """
    def __init__(self, parent, needs_cuadro=True):
        super().__init__(parent)
        # -----------------------------------------comunicación con Controllers--------------------------------
        self.init_controller = CommonWindowInitController()
        # -----------------------------------------atributos principales----------------------------------------
        self.parent = parent

        self.password = '777fer'

        self.resolution = self.get_screen_resolution()
        self.resolution_str = f'{self.resolution[0]}x{self.resolution[1]}'
        self.geometry(self.init_controller.calculate_window_resolution())

        self.img = parent.img
        self.icon: PhotoImage = ImageTk.PhotoImage(self.parent.img)
        self.theme = self.parent.theme

        #self.iconbitmap(self.icon_path) funcionaba en windows no en linux
        self.wm_iconphoto(False, self.icon) #marca en naranja pero funciona bien

        self.style.theme_use(self.theme)

        self.minsize(400,300)

        # ----------------------------otros atributos-----------------------
        self.alfabetico_checked = ttk.IntVar()

        # ----------------------------botón tema---------------------------
        self.str_modo = ttk.StringVar()
        self.str_modo.set('Modo claro')
        if self.theme == 'journal':
            self.str_modo.set('Modo oscuro')

        self.button_theme = ttk.Button(master=self, textvariable=self.str_modo, width=17, style='my.TButton',
                                       command=self.cambiar_modo)

        # ---------------------------botón menú----------------------------
        self.menu_button = ttk.Button(master=self, text='Volver al menú',  width=17, style='my.TButton',
                                 command=self.volver_al_menu)



        # -----------------------------------------------frames---------------------------------------------------
        self.frame = ttk.Frame(master=self)
        self.sub_frame = ttk.Frame(master=self.frame)

        # ----------------------------Botón orden alfabético---------------------------

        self.check = ttk.Checkbutton(self.frame, text="Mostrar en orden alfabético", variable=self.alfabetico_checked, command=self.toggle_busqueda_alfabetica)

        # --------------------------- cuadro ---------------------------

            # implementa tod0 el cuadro con la scrollbar
        if needs_cuadro:
            style = ttk.Style()
            style.configure('Treeview', rowheight=30)
            self.cuadro = ttk.Treeview(master=self.sub_frame, columns=("col1", "col2", "col3", "col4"))
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
            self.scrollbar = ttk.Scrollbar(self.sub_frame, orient="vertical", command=self.cuadro.yview)
            self.scrollbar.pack(side="right", fill="y")

            style_scroll = ttk.Style()
            style_scroll.configure("Vertical.TScrollbar", troughcolor="white")


    def toggle_busqueda_alfabetica(self):

        ordenado_alfabetico = True if int(self.alfabetico_checked.get()) == 1 else False

        if ordenado_alfabetico:  # 1 = marcado
            self.realizar_busqueda_alfabetica()
        else:  # 0 = no marcado
            self.realizar_busqueda()


    def realizar_busqueda_alfabetica(self):
        raise NotImplementedError("Subclasses should implement this method.")


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        """
        Perform a search or sorting operation based on the order_mode variable.
        To be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")


    def cerrar_ventana_alerta(self):
        raise NotImplementedError("Subclasses should implement this method.")


    def handle_correct_password(self, mode):
        """
        Handle the action to take when the correct password is entered.
        To be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")


    def solicit_password(self, mode):
        correct_password_introduced = False

        while not correct_password_introduced:
            dialog = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show="*")

            if dialog is None:
                break
            elif dialog == self.password:
                self.handle_correct_password(mode)
                correct_password_introduced = True
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")


    def cambiar_modo(self):
        if self.theme == 'journal':
            self.style.theme_use('darkly')
            self.parent.style.theme_use('darkly')
            self.theme = 'darkly'
            self.parent.theme = 'darkly'
            self.str_modo.set('Modo claro')


        else:
            self.style.theme_use('journal')
            self.theme = 'journal'
            self.str_modo.set('Modo oscuro')

        self.init_controller.tema_cambiado(self.theme)


    def get_screen_resolution(self):
        return self.init_controller.get_screen_resolution()


    def volver_al_menu(self):
        self.destroy()
        self.parent.maximizar()
        self.parent.deiconify()


    def pasar_al_cuadro(self, product_list: list[Producto]):
        # Borrar todas las filas existentes en el Treeview
        self.cuadro.delete(*self.cuadro.get_children())
        contador = 0
        # Añadir nuevas filas
        for product in product_list:
            tag = 'par' if contador % 2 == 0 else 'impar'
            self.cuadro.insert("", "end", text=product.producto, values=(product.codigo,
                                                                          f'${product.precio}', product.detalle,
                                                                          product.stock, product.id),
                               tags=tag)
            contador += 1
        return


    def pasar_unico_al_cuadro(self, product: dict):
        self.cuadro.delete(*self.cuadro.get_children())
        self.cuadro.insert("", "end", text=product['producto'], values=(product['codigo'],
                                                                      f'${product['precio']}', product['detalle'],
                                                                      product['stock'], product['id']),
                           tags=('par',))
        return


    def clean_treeview(self):
        self.cuadro.delete(*self.cuadro.get_children())


    def on_resize(self, event):
        new_width = event.width
        new_width = int(new_width * 0.9)

        self.cuadro.column("#0", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col1", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col2", width=int(new_width / 10), anchor="center")
        self.cuadro.column("col3", width=int(new_width * 3 / 10), anchor="center")
        self.cuadro.column("col4", width=int(new_width / 10), anchor="center")


    def render_view(self):
        raise NotImplementedError("Subclasses should implement this method.")


    def maximizar(self):
        try:
            self.attributes('-zoomed', True)
        except TclError:
            self.state('zoomed')


    @staticmethod
    def show_error(msg):
        messagebox.showerror('Ha ocurrido un error', msg)


    @staticmethod
    def show_message(msg):
        messagebox.showinfo('Atención', msg)