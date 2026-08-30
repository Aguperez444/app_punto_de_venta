from __future__ import annotations

import logging
from tkinter import PhotoImage, TclError, messagebox
from typing import TYPE_CHECKING

from PIL import Image, ImageTk
from tkrouter import RouteLinkButton, get_router
from tkrouter.views import StyledRoutedView
import ttkbootstrap as ttk

from app.infrastructure.config.auth_service import AuthService
from app.infrastructure.ui.tkinter.controllers.common.common_window_innit_controller import (
    CommonWindowInitController,
)

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.custom_widgets.customRouter import RouterOutlet

logger = logging.getLogger(__name__)


def ask_password_centered(parent_window, title: str, prompt: str) -> str | None:
    """Muestra un diálogo modal de contraseña centrado sobre `parent_window` (en su mismo monitor)."""
    result: dict[str, str | None] = {"value": None}

    dialog = ttk.Toplevel(parent_window)
    dialog.title(title)
    dialog.resizable(False, False)

    top_parent = parent_window.winfo_toplevel()
    CommonWindowInitController.center_window_on_parent(dialog, top_parent, 420, 185)

    frame = ttk.Frame(dialog, padding=18)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=prompt, font="Arial 11", wraplength=380, justify="center").pack(
        pady=(0, 10)
    )

    pwd_var = ttk.StringVar()
    entry = ttk.Entry(frame, textvariable=pwd_var, show="*", width=32)
    entry.pack(pady=(0, 14))

    btns = ttk.Frame(frame)
    btns.pack()

    def _on_ok(_event=None):
        result["value"] = pwd_var.get()
        dialog.destroy()

    def _on_cancel(_event=None):
        result["value"] = None
        dialog.destroy()

    ttk.Button(btns, text="Aceptar", bootstyle="primary", width=12, command=_on_ok).grid(
        row=0, column=0, padx=8
    )
    ttk.Button(btns, text="Cancelar", bootstyle="secondary", width=12, command=_on_cancel).grid(
        row=0, column=1, padx=8
    )

    dialog.bind("<Return>", _on_ok)
    dialog.bind("<Escape>", _on_cancel)
    dialog.protocol("WM_DELETE_WINDOW", _on_cancel)

    dialog.update_idletasks()
    # Re-centrar tras layout para precisión exacta en multi-monitor
    CommonWindowInitController.center_window_on_parent(
        dialog, top_parent, max(dialog.winfo_reqwidth(), 420), max(dialog.winfo_reqheight(), 175)
    )
    dialog.lift()
    dialog.grab_set()
    entry.focus_set()
    dialog.wait_window()
    return result["value"]


def _run_password_flow(owner_widget, auth_service: AuthService, on_success) -> None:
    top_parent = owner_widget.winfo_toplevel()

    if not auth_service.is_password_configured():
        new_pwd = ask_password_centered(
            top_parent,
            "Configurar contraseña",
            "No hay contraseña administrativa configurada.\nIngrese una nueva contraseña (mínimo 4 caracteres):",
        )
        if new_pwd is None:
            return
        confirm_pwd = ask_password_centered(
            top_parent,
            "Confirmar contraseña",
            "Vuelva a ingresar la contraseña:",
        )
        if confirm_pwd is None:
            return
        if new_pwd != confirm_pwd:
            messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=top_parent)
            return
        try:
            auth_service.set_password(new_pwd)
            messagebox.showinfo(
                "Contraseña configurada",
                "Contraseña administrativa guardada correctamente.",
                parent=top_parent,
            )
            on_success()
        except Exception as exc:
            messagebox.showerror("Error", str(exc), parent=top_parent)
        return

    while True:
        candidate = ask_password_centered(top_parent, "Contraseña", "Ingrese su contraseña:")
        if candidate is None:
            break
        if auth_service.verify_password(candidate):
            on_success()
            break
        messagebox.showerror("Error", "Contraseña incorrecta", parent=top_parent)


class BaseProjectWindow(ttk.Window):
    """Base class for project windows, providing common functionality."""

    def __init__(self, container=None):
        super().__init__()
        self.container = container
        self.auth_service = container.auth_service if container is not None else AuthService()
        self.init_controller = CommonWindowInitController(
            config_persistence=container.config if container is not None else None
        )

        self.icon_path = self.init_controller.get_icon_path()
        self.version = self.init_controller.get_version()
        self.window_geometry = self.init_controller.calculate_window_resolution()
        self.geometry(self.window_geometry)
        self.img = Image.open(self.icon_path)
        self.icon: PhotoImage = ImageTk.PhotoImage(self.img)
        self.theme = self.init_controller.obtener_tema_actual()

        self.minsize(400, 300)
        self.wm_iconphoto(False, self.icon)
        self.style.theme_use(self.theme)

        self.str_modo = ttk.StringVar()
        self.str_modo.set("Modo claro")
        if self.theme == "journal":
            self.str_modo.set("Modo oscuro")

    def solicit_password(self, mode):
        _run_password_flow(self, self.auth_service, lambda: self.handle_correct_password(mode))

    def handle_correct_password(self, mode):
        raise NotImplementedError("Subclasses should implement this method.")

    def cambiar_modo(self):
        if self.theme == "journal":
            self.style.theme_use("darkly")
            self.theme = "darkly"
            self.str_modo.set("Modo claro")
        else:
            self.style.theme_use("journal")
            self.theme = "journal"
            self.str_modo.set("Modo oscuro")
        self.init_controller.tema_cambiado(self.theme)

    def cerrar_ventana_alerta(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def show_error(self, msg):
        messagebox.showerror("Ha ocurrido un error", msg, parent=self)

    def report_callback_exception(self, exc, val, tb):
        logger.exception("Error no controlado en callback de Tkinter", exc_info=(exc, val, tb))
        self.show_error(f"Ocurrió un error inesperado: {val}")

    def maximizar(self):
        try:
            self.attributes("-zoomed", True)
        except TclError:
            self.state("zoomed")


class BaseProjectView(StyledRoutedView):
    """Base class for routed SPA views, providing common functionality."""

    def __init__(self, master: "RouterOutlet"):
        super().__init__(master)
        self.parent = master.parent
        self.container = getattr(self.parent, "container", None)
        self.auth_service = getattr(self.parent, "auth_service", AuthService())
        self.init_controller = CommonWindowInitController(
            config_persistence=self.container.config if self.container is not None else None
        )

        self.resolution = self.get_screen_resolution()
        self.resolution_str = f"{self.resolution[0]}x{self.resolution[1]}"

        self.str_modo = ttk.StringVar()
        self.str_modo.set("Modo claro")
        if self.parent.theme == "journal":
            self.str_modo.set("Modo oscuro")

        self.button_theme = ttk.Button(
            master=self,
            textvariable=self.str_modo,
            width=17,
            style="my.TButton",
            takefocus=False,
            command=self.cambiar_modo,
        )

        self.menu_button = RouteLinkButton(
            master=self,
            to="/",
            text="Volver al menú",
            width=17,
            style="my.TButton",
            takefocus=False,
        )

        self.frame = ttk.Frame(master=self)
        self.sub_frame = ttk.Frame(master=self.frame)

        self.parent.bind("<Escape>", self.volver_al_menu)

    def realizar_busqueda_alfabetica(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        raise NotImplementedError("Subclasses should implement this method.")

    def cerrar_ventana_alerta(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def handle_correct_password(self, mode):
        raise NotImplementedError("Subclasses should implement this method.")

    def solicit_password(self, mode):
        _run_password_flow(
            self.parent, self.auth_service, lambda: self.handle_correct_password(mode)
        )

    def cambiar_modo(self):
        if self.parent.theme == "journal":
            self.parent.style.theme_use("darkly")
            self.parent.theme = "darkly"
            self.str_modo.set("Modo claro")
        else:
            self.parent.style.theme_use("journal")
            self.parent.theme = "journal"
            self.str_modo.set("Modo oscuro")
        self.init_controller.tema_cambiado(self.parent.theme)

    def get_screen_resolution(self):
        return self.init_controller.get_screen_resolution()

    def clear_event(self, _varname=None, _index=None, _mode=None):
        pass

    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self.parent.bind("<Escape>", self.clear_event)
        self.parent.bind("<KeyRelease>", self.clear_event)
        get_router().navigate("/")

    def render_base(self):
        # Sin height fijo para respetar el padding natural de la fuente 'arial 12 bold'
        self.menu_button.place(x=15, y=14, anchor="nw")
        self.button_theme.place(relx=0.990, y=14, anchor="ne")

    def render_view(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def maximizar(self):
        try:
            self.parent.attributes("-zoomed", True)
        except TclError:
            self.parent.state("zoomed")

    def show_error(self, msg):
        messagebox.showerror("Ha ocurrido un error", msg, parent=self.parent)

    def show_message(self, msg):
        messagebox.showinfo("Atención", msg, parent=self.parent)


class BaseProjectPopupWindow(ttk.Toplevel):
    def __init__(self, parent, width: int | None = None, height: int | None = None):
        main_win = parent.parent if hasattr(parent, "parent") else parent
        super().__init__(main_win)
        self._main_window = main_win
        self.parent = parent
        self.container = getattr(parent, "container", getattr(main_win, "container", None))
        self.auth_service = getattr(parent, "auth_service", getattr(main_win, "auth_service", AuthService()))
        self.init_controller = CommonWindowInitController(
            config_persistence=self.container.config if self.container is not None else None
        )

        self.resolution = self.get_screen_resolution()
        self.resolution_str = f"{self.resolution[0]}x{self.resolution[1]}"

        self.img = main_win.img
        self.icon: PhotoImage = ImageTk.PhotoImage(self.img)
        self.theme = main_win.theme

        self.wm_iconphoto(False, self.icon)
        self.style.theme_use(self.theme)

        try:
            self.transient(main_win)
        except Exception:
            pass

        self.geometry(
            self.init_controller.calculate_popup_resolution(main_win, width=width, height=height)
        )
        self.minsize(600, 420)

        self.str_modo = ttk.StringVar()
        self.str_modo.set("Modo claro")
        if self.theme == "journal":
            self.str_modo.set("Modo oscuro")

        self.button_theme = ttk.Button(
            master=self,
            textvariable=self.str_modo,
            width=17,
            style="my.TButton",
            command=self.cambiar_modo,
        )
        self.menu_button = ttk.Button(
            master=self,
            text="Volver al menú",
            width=17,
            style="my.TButton",
            command=self.volver_al_menu,
        )

        self.frame = ttk.Frame(master=self)
        self.sub_frame = ttk.Frame(master=self.frame)

        self.bind("<Escape>", self.volver_al_menu)
        self.bind("<Return>", self.confirm_action)

        self.buttons_frame = None
        self.input_frame = None
        self.entry = None
        self.label_input = None
        self.button_confirm = None
        self.button_cancel = None
        self.sub_label_alerta = None
        self.label_alerta = None
        self.relleno_superior = None

    def center_on_parent(self, width: int, height: int) -> None:
        self.init_controller.center_window_on_parent(self, self._main_window, width, height)

    def confirm_action(self, _varname=None, _index=None, _mode=None):
        raise NotImplementedError("Subclasses should implement this method.")

    def realizar_busqueda_alfabetica(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def realizar_busqueda(self, _varname=None, _index=None, _mode=None):
        raise NotImplementedError("Subclasses should implement this method.")

    def cerrar_ventana_alerta(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def handle_correct_password(self, mode):
        raise NotImplementedError("Subclasses should implement this method.")

    def solicit_password(self, mode):
        _run_password_flow(self, self.auth_service, lambda: self.handle_correct_password(mode))

    def cambiar_modo(self):
        if self.theme == "journal":
            self.style.theme_use("darkly")
            self._main_window.style.theme_use("darkly")
            self.theme = "darkly"
            self._main_window.theme = "darkly"
            self.str_modo.set("Modo claro")
        else:
            self.style.theme_use("journal")
            self._main_window.style.theme_use("journal")
            self.theme = "journal"
            self._main_window.theme = "journal"
            self.str_modo.set("Modo oscuro")
        self.init_controller.tema_cambiado(self.theme)

    def get_screen_resolution(self):
        return self.init_controller.get_screen_resolution()

    def volver_al_menu(self, _varname=None, _index=None, _mode=None):
        self.destroy()

    def maximizar(self):
        try:
            self.attributes("-zoomed", True)
        except TclError:
            self.state("zoomed")

    def show_error(self, msg):
        messagebox.showerror("Ha ocurrido un error", msg, parent=self)

    def show_message(self, msg):
        messagebox.showinfo("Atención", msg, parent=self)

    def render_view(self):
        self.relleno_superior.pack(side="top")
        self.label_alerta.pack()
        self.sub_label_alerta.pack()
        self.button_cancel.grid(row=0, column=0, padx=15)
        self.button_confirm.grid(row=0, column=1, padx=15)
        self.label_input.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.input_frame.pack()
        self.buttons_frame.pack(pady=15)
