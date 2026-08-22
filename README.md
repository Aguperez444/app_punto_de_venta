# Catálogo de Productos – Gestión de inventario y ventas (Hexagonal + Tkinter + SQLAlchemy 2.0)

Aplicación de escritorio para farmacia/mostrador para administrar productos, stock, precios y ventas. Construida en Python con **Arquitectura Hexagonal (Ports & Adapters)** estricta, UI SPA en Tkinter/ttkbootstrap, persistencia en SQLAlchemy 2.0 (PostgreSQL y SQLite) y migraciones con Alembic.

---

## Tecnologías y librerías

- Lenguaje: **Python 3.13**
- UI: **Tkinter** + **ttkbootstrap** + **tkrouter** (SPA con navegación por teclado y temas claro/oscuro)
- ORM/DB: **SQLAlchemy 2.0** + **PostgreSQL (`psycopg`)** / **SQLite** + **Alembic**
- Patrones: **Arquitectura Hexagonal**, Unit of Work con commit explícito, Repositorios, Composition Root (`AppContainer`), DTOs, Value Objects inmutables
- Testing: **pytest**, pytest-cov, pytest-mock, freezegun, faker

---

## Funcionalidades principales

- **Gestión de productos**
  - Alta, edición y baja lógica (archivo y reactivación preservando integridad referencial de ventas históricas)
  - Búsqueda con debounce (250 ms), orden alfabético, búsqueda por código de barras y contador de resultados
  - Edición individual y masiva de precios con porcentajes predefinidos o **porcentaje personalizado** con vista previa
  - Ajuste de stock en 3 modos (**Sumar**, **Restar**, **Fijar exacto**) y listado de productos sin stock / con stock negativo
  - **Regla de negocio de stock negativo:** se permite vender productos incluso sin stock cargado (quedando negativo con aviso informativo en pantalla) para no frenar la atención en mostrador
- **Gestión de ventas y carrito inteligente**
  - **Venta rápida (1 producto):** al abrir un producto con el carrito vacío, presionar `Enter` registra la venta directa sin pasos extra
  - **Carrito multi-producto:** al agregar un producto al carrito, la acción por defecto con `Enter` cambia automáticamente a *"Añadir al carrito"* hasta finalizar o vaciar el carrito (`F2` abre el checkout)
  - Registro atómico de ventas con múltiples ítems y precisión decimal (`ROUND_HALF_UP`)
  - Consultas de ventas por día, mes y rango, **popup de detalle completo** por venta y **exportación a CSV** (ventas y lista de faltantes)
- **Seguridad, configuración y observabilidad**
  - Contraseña administrativa protegida con `hashlib.scrypt` + salt aleatorio (sin contraseñas hardcodeadas)
  - Configuración en `config.json` (con migración automática desde `config.txt`), soporte para `DATABASE_URL` por variable de entorno y asistente de conexión PostgreSQL/SQLite con prueba de conectividad y migraciones Alembic
  - Logging estructurado rotativo en archivo (`catalogo/logs/app.log`) y captura global de excepciones

---

## Arquitectura (Hexagonal / Ports & Adapters)

- **Domain (`app/domain/`)**: 100% puro, sin dependencias externas. Entidades (`Producto`, `Venta`, `DetalleVenta`), Value Objects inmutables (`Precio`, `Stock`) y jerarquía `DomainValidationError`.
- **Application (`app/application/`)**: Casos de uso (`AddProduct`, `EditProductInfo`, `DeleteProduct`, `RestoreProduct`, `EditStock`, `UpdatePrice`, `RegisterSale`, `QueryProducts`, `QuerySales`), servicio `SaleCart`, DTOs (`ProductDTO`, `SaleSummaryDTO`, `SaleDetailDTO`) y puertos (`IProductoRepository`, `ISaleRepository`, `IUnitOfWork`, `IClock`).
- **Infrastructure (`app/infrastructure/`)**:
  - `database/sqlalchemy/`: modelos ORM (`Numeric(12, 2)`, índices, `activo`), mappers, repositorios SQLAlchemy 2.0, `SqlAlchemyUnitOfWork` y `engine_factory` multidialecto.
  - `config/`: `ConfigFilesPersistence` (`config.json`), `AuthService` (`scrypt`) y `logging_config`.
  - `di/`: `AppContainer` (Composition Root con inicialización perezosa).
  - `export/`: `CsvExporter` compatible con Excel (`utf-8-sig`).
  - `ui/tkinter/`: vistas SPA, popups, widgets reutilizables y controladores con inyección de dependencias.
- **Runners (`app/runners/Programa_catalogo.py`)**: punto de entrada que inicializa logging, `AppContainer`, primer arranque y `MainMenuWindow`.

---

## Instalación y ejecución

```bash
pip install -r requirements.txt
```

Ejecutar desde la raíz del proyecto:

```bash
python -m app.runners.Programa_catalogo
```

También podés definir la base de datos por variable de entorno:

```bash
DATABASE_URL="postgresql+psycopg://usuario:clave@127.0.0.1:5432/farmacia" python -m app.runners.Programa_catalogo
```

### Migraciones (Alembic)

```bash
DATABASE_URL="sqlite:///productos.db" alembic upgrade head
```

---

## Testing

```bash
# Suite completa con cobertura
pytest

# Solo unitarios
pytest -m unit tests/unit

# Solo integración
pytest -m integration tests/integration
```
