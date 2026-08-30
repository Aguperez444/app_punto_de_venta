from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import quote_plus
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox

from app.infrastructure.database.sqlalchemy.engine_factory import test_db_connection
from app.infrastructure.database.sqlalchemy.migrations_runner import run_alembic_upgrade

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.controllers.common.program_start_controller import (
        ProgramStartController,
    )

logger = logging.getLogger(__name__)


def build_postgres_url(host: str, port: str, database: str, user: str, password: str) -> str:
    clean_host = host.strip()
    clean_port = port.strip() or "5432"
    clean_db = database.strip()
    clean_user = quote_plus(user.strip())
    clean_pass = quote_plus(password)
    if not clean_host or not clean_db or not clean_user:
        raise ValueError("Host, base de datos y usuario son obligatorios para PostgreSQL.")
    return f"postgresql+psycopg://{clean_user}:{clean_pass}@{clean_host}:{clean_port}/{clean_db}"


class FindBddWindow(ttk.Window):
    """Asistente de configuración inicial de conexión a Base de Datos (PostgreSQL o SQLite)."""

    def __init__(self, puntero_controller: "ProgramStartController", initial_url: str = ""):
        super().__init__(themename="journal")
        self.title("Configurar conexión a la base de datos")
        self.geometry("820x500")
        self.minsize(780, 480)

        self.controller = puntero_controller
        self.status_var = ttk.StringVar(value="Configure una conexión PostgreSQL o SQLite local.")

        # PostgreSQL vars
        self.pg_host = ttk.StringVar(value="localhost")
        self.pg_port = ttk.StringVar(value="5432")
        self.pg_db = ttk.StringVar(value="farmacia")
        self.pg_user = ttk.StringVar(value="postgres")
        self.pg_pass = ttk.StringVar(value="")
        self.pg_raw_url = ttk.StringVar(
            value=initial_url if initial_url.startswith("postgresql") else ""
        )

        # SQLite vars
        self.sqlite_path = ttk.StringVar(
            value=initial_url.replace("sqlite:///", "")
            if initial_url.startswith("sqlite:///")
            else ""
        )

        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Label(
            self, text="Conexión a Base de Datos", font="Arial 16 bold"
        )
        header.pack(pady=(14, 6))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=8)

        # --- Tab PostgreSQL ---
        pg_tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(pg_tab, text="PostgreSQL")

        fields = [
            ("Host / IP:", self.pg_host, False),
            ("Puerto:", self.pg_port, False),
            ("Base de datos:", self.pg_db, False),
            ("Usuario:", self.pg_user, False),
            ("Contraseña:", self.pg_pass, True),
        ]
        for idx, (label, var, secret) in enumerate(fields):
            ttk.Label(pg_tab, text=label, width=16, anchor="e").grid(
                row=idx, column=0, padx=(0, 8), pady=4, sticky="e"
            )
            entry_kwargs = {"show": "*"} if secret else {}
            ttk.Entry(pg_tab, textvariable=var, width=38, **entry_kwargs).grid(
                row=idx, column=1, pady=4, sticky="ew"
            )

        ttk.Separator(pg_tab).grid(row=5, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Label(pg_tab, text="O URL completa:", width=16, anchor="e").grid(
            row=6, column=0, padx=(0, 8), pady=4, sticky="e"
        )
        ttk.Entry(pg_tab, textvariable=self.pg_raw_url, width=38).grid(
            row=6, column=1, pady=4, sticky="ew"
        )
        pg_tab.columnconfigure(1, weight=1)

        # --- Tab SQLite ---
        sqlite_tab = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(sqlite_tab, text="SQLite local")

        ttk.Label(
            sqlite_tab,
            text="Seleccione un archivo .db/.sqlite existente o cree uno nuevo:",
            font="Arial 11",
        ).pack(anchor="w", pady=(8, 8))

        path_frame = ttk.Frame(sqlite_tab)
        path_frame.pack(fill="x", pady=6)
        ttk.Entry(path_frame, textvariable=self.sqlite_path).pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )
        ttk.Button(
            path_frame, text="Explorar...", bootstyle="info", command=self.abrir_explorador
        ).pack(side="right")

        # --- Status & Actions ---
        ttk.Label(
            self, textvariable=self.status_var, font="Arial 10 italic", wraplength=560
        ).pack(pady=(4, 6))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=(4, 14))

        ttk.Button(
            btn_frame,
            text="Probar conexión",
            bootstyle="info",
            width=18,
            command=self.probar_conexion,
        ).grid(row=0, column=0, padx=6)
        ttk.Button(
            btn_frame,
            text="Aplicar migraciones",
            bootstyle="warning",
            width=18,
            command=self.aplicar_migraciones,
        ).grid(row=0, column=1, padx=6)
        ttk.Button(
            btn_frame,
            text="Guardar y continuar",
            bootstyle="success",
            width=20,
            command=self.confirmar_ruta,
        ).grid(row=0, column=2, padx=6)

    def _get_selected_url(self) -> str:
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            raw = self.pg_raw_url.get().strip()
            if raw:
                return raw
            return build_postgres_url(
                self.pg_host.get(),
                self.pg_port.get(),
                self.pg_db.get(),
                self.pg_user.get(),
                self.pg_pass.get(),
            )
        path = self.sqlite_path.get().strip()
        if not path:
            raise ValueError("Seleccione o ingrese una ruta de archivo SQLite válida.")
        if path.startswith("sqlite:///"):
            return path
        return f"sqlite:///{path}"

    def abrir_explorador(self):
        selected = filedialog.askopenfilename(
            title="Seleccionar base de datos SQLite",
            filetypes=[("SQLite DB", "*.db *.sqlite *.sqlite3"), ("Todos los archivos", "*.*")],
        )
        if selected:
            self.sqlite_path.set(selected)
            self.status_var.set(f"Archivo seleccionado: {selected}")

    def probar_conexion(self):
        try:
            url = self._get_selected_url()
        except ValueError as exc:
            messagebox.showerror("Datos incompletos", str(exc), parent=self)
            return

        ok, msg = test_db_connection(url)
        self.status_var.set(msg)
        if ok:
            messagebox.showinfo("Conexión exitosa", msg, parent=self)
        else:
            messagebox.showerror("Error de conexión", msg, parent=self)

    def aplicar_migraciones(self):
        try:
            url = self._get_selected_url()
        except ValueError as exc:
            messagebox.showerror("Datos incompletos", str(exc), parent=self)
            return

        ok, msg = run_alembic_upgrade(url)
        self.status_var.set(msg)
        if ok:
            messagebox.showinfo("Migraciones", msg, parent=self)
        else:
            messagebox.showerror("Error en migraciones", msg, parent=self)

    def confirmar_ruta(self):
        try:
            url = self._get_selected_url()
        except ValueError as exc:
            messagebox.showerror("Ruta incompleta", str(exc), parent=self)
            return

        self.controller.new_bdd_route_added(url)
        self.destroy()
