import ttkbootstrap as ttk
from tkinter import simpledialog, messagebox, PhotoImage

from tkrouter import RouteLinkButton, get_router

from app.infrastructure.ui.tkinter.controllers.common.common_window_innit_controller import CommonWindowInitController
from PIL import Image, ImageTk
from tkinter import TclError

from tkrouter.views import StyledRoutedView


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.custom_widgets.customRouter import RouterOutlet

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
        self.icon_path = self.init_controller.get_icon_path() # get the path to the icon
        self.version = self.init_controller.get_version() # get the program version
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


class BaseProjectView(StyledRoutedView):
    """
    Base class for project topLevel windows, providing common functionality.
    """
    def __init__(self, master: 'RouterOutlet'):
        super().__init__(master)
        # -----------------------------------------comunicación con Controllers--------------------------------
        self.init_controller = CommonWindowInitController()
        # -----------------------------------------atributos principales----------------------------------------
        self.password = '777fer'

        self.parent = master.parent

        self.resolution = self.get_screen_resolution()
        self.resolution_str = f'{self.resolution[0]}x{self.resolution[1]}'

        # ----------------------------botón tema---------------------------
        self.str_modo = ttk.StringVar()
        self.str_modo.set('Modo claro')
        if self.parent.theme == 'journal':
            self.str_modo.set('Modo oscuro')

        self.button_theme = ttk.Button(master=self, textvariable=self.str_modo, width=17, style='my.TButton',
                                       command=self.cambiar_modo)

        # ---------------------------botón menú----------------------------
        self.menu_button = RouteLinkButton(master=self, to='/', text='Volver al menú',  width=17, style='my.TButton')


        # -----------------------------------------------frames---------------------------------------------------
        self.frame = ttk.Frame(master=self)
        self.sub_frame = ttk.Frame(master=self.frame)



        # -----------------------------------------------gestion de eventos----------------------------------------
        self.parent.bind("<Escape>", self.volver_al_menu)


    def realizar_busqueda_alfabetica(self):
        raise NotImplementedError("Subclasses should implement this method.")


    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
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
        if self.parent.theme == 'journal':
            self.parent.style.theme_use('darkly')
            self.parent.style.theme_use('darkly')
            self.parent.theme = 'darkly'
            self.parent.theme = 'darkly'
            self.str_modo.set('Modo claro')


        else:
            self.parent.style.theme_use('journal')
            self.parent.theme = 'journal'
            self.str_modo.set('Modo oscuro')

        self.init_controller.tema_cambiado(self.parent.theme)


    def get_screen_resolution(self):
        return self.init_controller.get_screen_resolution()


    def clear_event(self, _varname=None, _index=None, _mode=None):
        pass


    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self.parent.bind("<Escape>", self.clear_event) # evita que se siga recargando el menu con esc al volver al menu
        self.parent.bind("<KeyRelease>", self.clear_event)
        get_router().navigate('/')


    def render_base(self):
        self.menu_button.place(x=15, rely=0.017, anchor='nw', height=35)
        self.button_theme.place(relx=0.990, rely=0.017, height=35, anchor='ne')


    def render_view(self):
        raise NotImplementedError("Subclasses should implement this method.")


    def maximizar(self):
        try:
            self.parent.attributes('-zoomed', True)
        except TclError:
            self.parent.state('zoomed')


    @staticmethod
    def show_error(msg):
        messagebox.showerror('Ha ocurrido un error', msg)


    @staticmethod
    def show_message(msg):
        messagebox.showinfo('Atención', msg)


class BaseProjectPopupWindow(ttk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent.parent)
        # -----------------------------------------comunicación con Controllers--------------------------------
        self.init_controller = CommonWindowInitController()
        # -----------------------------------------atributos principales----------------------------------------
        self.parent = parent

        self.password = '777fer'

        self.resolution = self.get_screen_resolution()
        self.resolution_str = f'{self.resolution[0]}x{self.resolution[1]}'

        self.img = parent.parent.img
        self.icon: PhotoImage = ImageTk.PhotoImage(self.img)
        self.theme = self.parent.parent.theme

        #self.iconbitmap(self.icon_path) funcionaba en windows no en linux
        self.wm_iconphoto(False, self.icon)

        self.style.theme_use(self.theme)


        self.geometry(self.init_controller.calculate_popup_resolution(self.parent.parent))

        self.minsize(600,500)

        # -------------------------------------- buttons -------------------------------------------
        # ---------------------------- button theme ---------------------------
        self.str_modo = ttk.StringVar()
        self.str_modo.set('Modo claro')
        if self.theme == 'journal':
            self.str_modo.set('Modo oscuro')

        self.button_theme = ttk.Button(master=self, textvariable=self.str_modo, width=17, style='my.TButton',
                                       command=self.cambiar_modo)

        # --------------------------- button menu ----------------------------
        self.menu_button = ttk.Button(master=self, text='Volver al menú',  width=17, style='my.TButton',
                                 command=self.volver_al_menu)



        # -----------------------------------------------frames---------------------------------------------------
        self.frame = ttk.Frame(master=self)
        self.sub_frame = ttk.Frame(master=self.frame)


        # -----------------------------------------------gestion de eventos----------------------------------------
        self.bind("<Escape>", self.volver_al_menu)
        self.bind('<Return>', self.confirm_action)


        self.buttons_frame = None
        self.input_frame = None
        self.entry = None
        self.label_input = None
        self.button_confirm = None
        self.button_cancel = None
        self.sub_label_alerta = None
        self.label_alerta = None
        self.relleno_superior = None
        self.parent = parent



    def confirm_action(self, _varname=None, _index=None, _mode=None):
        raise NotImplementedError("Subclasses should implement this method.")


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


    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self.destroy()


    def maximizar(self):
        try:
            self.attributes('-zoomed', True)
        except TclError:
            self.state('zoomed')


    def show_error(self, msg):
        messagebox.showerror('Ha ocurrido un error', msg, parent=self)


    def show_message(self, msg):
        messagebox.showinfo('Atención', msg, parent=self)


    def render_view(self):
        self.relleno_superior.pack(side='top')
        self.label_alerta.pack()
        self.sub_label_alerta.pack()
        self.button_cancel.grid(row=0, column=0, padx=15)
        self.button_confirm.grid(row=0, column=1, padx=15)
        self.label_input.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.input_frame.pack()
        self.buttons_frame.pack(pady=15)