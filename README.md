# 📦 Catálogo de Productos – Gestión de inventario y ventas (Hexagonal + Tkinter + SQLAlchemy)

Aplicación de escritorio para administrar productos, stock, precios y ventas. Construida en Python con arquitectura Hexagonal (Ports & Adapters), UI en Tkinter y persistencia con SQLAlchemy/PostgresSQL.

---

## ⚙️ Tecnologías y librerías

- Lenguaje: **Python 3.13**
- UI: **Tkinter** + **ttkbootstrap** + **tkrouter** (estilos modernos)
- ORM/DB: **SQLAlchemy + PostgresSQL**
- Patrones: **Arquitectura Hexagonal**, Unit of Work, Repositorios, Value Objects
- Testing: **pytest**, pytest-cov, pytest-mock, freezegun, faker
- Otros: screeninfo (soporte de pantallas), iconos estáticos en PNG/ICO

---

## 🚀 Funcionalidades principales

- **Gestión de productos**
  - Alta, baja y modificación de productos
  - Edición individual y masiva (precio/stock)
  - Búsqueda y listados ordenados alfabéticamente
  - Detección de productos sin stock
- **Gestión de ventas**
  - Registro de ventas con detalles (producto, cantidad, precio unitario)
  - Cálculo de subtotales y total con precisión decimal
  - Consultas por día, rango y mes
- **Persistencia**
  - BDD PostgresSQL
  - Se provee una BDD en SQLite con la estructura que debe tener la BDD
  - Unidad de trabajo (UoW) para transacciones consistentes
- **Experiencia de usuario**
  - Ventanas y popups con validaciones de dominio
  - Soporte de temas/estilos (ttkbootstrap)
  - UI responsive
  - UI navegable mediante teclado

---


## 🛠️ Arquitectura (Hexagonal / Ports & Adapters)

- **Domain**
  - Entidades y Value Objects: Producto, Venta, DetalleVenta, Precio, Stock
  - Reglas de negocio puras y excepciones de dominio
- **Application**
  - Use Cases: AddProduct, EditProductInfo, EditStock, UpdatePrice, RegisterSale, QueryProducts, QuerySales
  - Puertos (ports) para repositorios y Unidad de Trabajo (IProductoRepository, ISaleRepository, IUnitOfWork)
- **Infrastructure**
  - Adaptadores concretos: SQLAlchemy ORM, Repositorios (ProductoRepositoryImpl, SaleRepositoryImpl)
  - Unit of Work real (SqlAlchemyUnitOfWork) y fábrica (uow_factory)
  - Configuración de ruta de base de datos (ConfigFilesPersistence)
- **UI (Adapter)**
  - Tkinter + ttkbootstrap: vistas y controladores por acción (alta de producto, edición, registro de venta, listados)
- **Runners**
  - Punto de entrada de la aplicación de escritorio (app/runners/Programa_catalogo.py)

Beneficios: separación estricta de capas, testabilidad (use cases con fakes), independencia de framework/DB.


## 📂 Estructura del proyecto (resumen)

```
.
├── app/
│   ├── application/
│   │   ├── building_blocks/
│   │   ├── ports/
│   │   └── use_cases/
│   ├── domain/
│   │   ├── models/
│   │   └── custom_errors.py
│   ├── infrastructure/
│   │   ├── config/
│   │   ├── database/sqlalchemy/
│   │   │   ├── repositories/
│   │   │   ├── uow_factory.py
│   │   │   └── unit_of_work_impl.py
│   │   └── ui/tkinter/
│   │       ├── controllers/
│   │       ├── custom_widgets/
│   │       └── views/
│   └── runners/Programa_catalogo.py
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   └── application/use_cases/
│   └── integration/
├── productos.db
├── pytest.ini
├── requirements.txt
├── TODO.txt
└── README.md
```

Consulta el árbol completo en el repositorio para ver todos los módulos (repositorios, controladores y vistas específicas).

---

## 📦 Instalación y requisitos

- Python 3.13
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

Requisitos mínimos en requirements.txt: SQLAlchemy, ttkbootstrap, screeninfo, pytest y complementos si vas a ejecutar tests.

---

## ▶️ Ejecución de la aplicación

Desde la raíz del proyecto:

```bash
python app/runners/Programa_catalogo.py
```

En el primer arranque se solicitará la ruta de la base de datos. Se espera una direccion de postgres.   
(ejemplo: postgresql+psycopg://miusuario:micontra@192.168.1.255:5432/mibasedatos)

---

## 🧪 Testing

- Ejecutar toda la suite:

```bash
pytest
```

- Ejecutar unit tests únicamente:

```bash
pytest -m unit tests/unit
```

- Ejecutar integración:

```bash
pytest -m integration tests/integration
```

La configuración de pytest (pytest.ini) incluye cobertura con pytest-cov y marcadores unit/integration.

---

## 🔌 Detalles técnicos relevantes

- Precisión monetaria: cálculos con Decimal y redondeo HALF_UP a 2 decimales
- Unit of Work: garantiza commit/rollback y cierre de sesión por acción
- Repositorios: consultas, filtros y actualizaciones en SQLAlchemy; mapeos con ORM propio
- Value Objects: Precio y Stock encapsulan validación y operaciones numéricas

---

## 🗺️ Roadmap breve

- Mejoras en validaciones de UI y mensajes de error
- Logging estructurado y empaquetado para distribución

---

## 👨‍💻 Autor
Proyecto personal en desarrollo como laboratorio de buenas prácticas, patrones de diseño y arquitectura de software.
