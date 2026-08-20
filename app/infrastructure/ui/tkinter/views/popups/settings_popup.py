from __future__ import annotations

from tkinter import filedialog, messagebox
import ttkbootstrap as ttk

from app.domain.custom_errors import DomainValidationError
from app.infrastructure.database.sqlalchemy.engine_factory import test_db_connection
from app.infrastructure.ui.tkinter.views.abstract.base_window_abstract_class import (
    BaseProjectPopupWindow,
)
from app.infrastructure.ui.tkinter.views.windows.find_bdd_window import run_alembic_upgrade


class SettingsPopup(BaseProjectPopupWindow):
    """Popup de configuración accesible desde el menú principal (BDD + Contraseña admin)."""

    def __init__(self, parent):
        # parent es MainMenuWindow (BaseProjectWindow); BaseProjectPopupWindow espera parent.parent
        # adaptamos soportando tanto MainMenuWindow como vistas ruteadas
        self._main_window = parent if hasattr(parent, "style") else parent.parent
        ttk.Toplevel.__init__(self, self._main_window)
        self.parent = self._main_window
        self.container = getattr(self._main_window, "container", None)
        self.auth_service = self._main_window.auth_service
        self.config = (
            self.container.config
            if self.container is not None
            else self._main_window.init_controller.config_pointer
        )

        self.title("Configuración del Sistema")
        self.geometry("640x480")
        self.minsize(600, 440)
        self.bind("<Escape>", lambda _e: self.destroy())
        self.focus_set()

        self.db_url_var = ttk.StringVar(value=self.config.get_ruta_bdd())
        self.db_status_var = ttk.StringVar(value="")

        self.current_pwd_var = ttk.StringVar(value="")
        self.new_pwd_var = ttk.StringVar(value="")
        self.confirm_pwd_var = ttk.StringVar(value="")

        self._build_ui()

    def _build_ui(self) -> None:
        ttk.Label(self, text="Configuración", font="Arial 18 bold").pack(pady=(14, 6))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=8)

        # --- Tab Base de Datos ---
        db_tab = ttk.Frame(notebook, padding=16)
        notebook.add(db_tab, text="Base de Datos")

        ttk.Label(
            db_tab,
            text="URL de conexión SQLAlchemy (PostgreSQL o SQLite):",
            font="Arial 11 bold",
        ).pack(anchor="w", pady=(0, 6))

        url_frame = ttk.Frame(db_tab)
        url_frame.pack(fill="x", pady=4)
        ttk.Entry(url_frame, textvariable=self.db_url_var).pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )
        ttk.Button(
            url_frame, text="Archivo SQLite...", style="secondary", command=self._browse_sqlite
        ).pack(side="right")

        ttk.Label(
            db_tab,
            text="Ejemplo PostgreSQL: postgresql+psycopg://usuario:clave@127.0.0.1:5432/farmacia",
            font="Arial 9 italic",
        ).pack(anchor="w", pady=(2, 10))

        db_btns = ttk.Frame(db_tab)
        db_btns.pack(pady=8)
        ttk.Button(
            db_btns, text="Probar conexión", style="info", width=18, command=self._test_connection
        ).grid(row=0, column=0, padx=6)
        ttk.Button(
            db_btns,
            text="Aplicar migraciones",
            style="warning",
            width=18,
            command=self._run_migrations,
        ).grid(row=0, column=1, padx=6)
        ttk.Button(
            db_btns, text="Guardar URL", style="success", width=16, command=self._save_db_url
        ).grid(row=0, column=2, padx=6)

        ttk.Label(
            db_tab, textvariable=self.db_status_var, font="Arial 10 italic", wraplength=540
        ).pack(pady=8)

        # --- Tab Seguridad / Contraseña ---
        sec_tab = ttk.Frame(notebook, padding=16)
        notebook.add(sec_tab, text="Seguridad")

        is_configured = self.auth_service.is_password_configured()
        row = 0
        if is_configured:
            ttk.Label(sec_tab, text="Contraseña actual:", width=20, anchor="e").grid(
                row=row, column=0, padx=(0, 8), pady=6, sticky="e"
            )
            ttk.Entry(sec_tab, textvariable=self.current_pwd_var, show="*", width=28).grid(
                row=row, column=1, pady=6, sticky="w"
            )
            row += 1

        ttk.Label(sec_tab, text="Nueva contraseña:", width=20, anchor="e").grid(
            row=row, column=0, padx=(0, 8), pady=6, sticky="e"
        )
        ttk.Entry(sec_tab, textvariable=self.new_pwd_var, show="*", width=28).grid(
            row=row, column=1, pady=6, sticky="w"
        )
        row += 1

        ttk.Label(sec_tab, text="Confirmar contraseña:", width=20, anchor="e").grid(
            row=row, column=0, padx=(0, 8), pady=6, sticky="e"
        )
        ttk.Entry(sec_tab, textvariable=self.confirm_pwd_var, show="*", width=28).grid(
            row=row, column=1, pady=6, sticky="w"
        )
        row += 1

        ttk.Button(
            sec_tab,
            text="Guardar contraseña",
            style="success",
            width=22,
            command=self._save_password,
        ).grid(row=row, column=0, columnspan=2, pady=14)

        ttk.Button(self, text="Cerrar", style="secondary", width=16, command=self.destroy).pack(
            pady=(4, 14)
        )

    def _browse_sqlite(self):
        selected = filedialog.askopenfilename(
            parent=self,
            title="Seleccionar base de datos SQLite",
            filetypes=[("SQLite DB", "*.db *.sqlite *.sqlite3"), ("Todos los archivos", "*.*")],
        )
        if selected:
            self.db_url_var.set(f"sqlite:///{selected}")

    def _test_connection(self):
        url = self.db_url_var.get().strip()
        ok, msg = test_db_connection(url)
        self.db_status_var.set(msg)
        if ok:
            messagebox.showinfo("Conexión exitosa", msg, parent=self)
        else:
            messagebox.showerror("Error de conexión", msg, parent=self)

    def _run_migrations(self):
        url = self.db_url_var.get().strip()
        ok, msg = run_alembic_upgrade(url)
        self.db_status_var.set(msg)
        if ok:
            messagebox.showinfo("Migraciones", msg, parent=self)
        else:
            messagebox.showerror("Error en migraciones", msg, parent=self)

    def _save_db_url(self):
        url = self.db_url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "La URL de conexión no puede estar vacía.", parent=self)
            return
        if self.container is not None:
            self.container.reload_database(url)
        else:
            self.config.set_new_bbd_route_in_config(url)
        self.db_status_var.set("URL guardada y conexión recargada.")
        messagebox.showinfo("Guardado", "Conexión actualizada correctamente.", parent=self)

    def _save_password(self):
        new_pwd = self.new_pwd_var.get()
        confirm_pwd = self.confirm_pwd_var.get()
        if new_pwd != confirm_pwd:
            messagebox.showerror("Error", "Las contraseñas nuevas no coinciden.", parent=self)
            return
        try:
            if self.auth_service.is_password_configured():
                self.auth_service.change_password(self.current_pwd_var.get(), new_pwd)
            else:
                self.auth_service.set_password(new_pwd)
            messagebox.showinfo("Seguridad", "Contraseña actualizada correctamente.", parent=self)
            self.current_pwd_var.set("")
            self.new_pwd_var.set("")
            self.confirm_pwd_var.set("")
        except DomainValidationError as exc:
            messagebox.showerror("Error", str(exc), parent=self)
