# 📦 Catálogo de Productos – MVC con Tkinter + SQLAlchemy

Aplicación de escritorio para la gestión de inventario, ventas y precios, desarrollada en **Python 3.13**, utilizando:

## ⚙️ Tecnologías

- **Python 3.13**

- **Tkinter** + [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) → Interfaz gráfica moderna y responsiva  
- **SQLAlchemy ORM** → Acceso a base de datos relacional  
- **SQLite3** → Persistencia local
- Arquitectura **MVC** → Separación estricta en *Views*, *Controllers*, *Services*, *Repositories* y *Models*  

---

## 🚀 Funcionalidades principales

- **Gestión de productos**  
  - Alta, baja y modificación de productos  
  - Edición de información individual o masiva  
  - Actualización de precios (por porcentaje o valor fijo)  
  - Control de stock y listado de productos agotados  

- **Gestión de ventas**  
  - Registro rápido de ventas con control de cantidad  
  - Cálculo automático de subtotales y totales  
  - Historial de ventas diarias y mensuales  
  - Asociación de detalles de venta (producto ↔ venta)  

- **Persistencia flexible**  
  - Base de datos SQLite lista para usar (`productos.db`)  
  - Configuración persistida en archivos externos (`Persistence/config_files_persistance.py`)   

- **Experiencia de usuario**  
  - Interfaz responsiva con detección automática de resolución de pantalla  
  - Manejo de temas y estilos configurables  
  - Ventanas emergentes y validaciones de dominio  

---

## 📂 Estructura del proyecto

```
.
├── Controllers/        # Coordinan Views ↔ Services
├── Models/             # Entidades SQLAlchemy (Producto, Venta, DetalleVenta)
├── Persistence/        # Sesiones DB, Repositories, config y migraciones
├── Services/           # Lógica de negocio y validaciones
├── Views/              # Interfaces gráficas (Tkinter + ttkbootstrap)
├── custom_errors.py    # Excepciones de dominio
├── Programa_catalogo.py # Entry point
├── productos.db        # Base de datos SQLite (ejemplo)
└── TODO.txt            # Funcionalidades pendientes de implementar
└── requirements.txt   # Dependencias del proyecto
└── README.md
```

---

## ⚙️ Requisitos

- Python **3.13+**
- Dependencias (instalar con `pip install -r requirements.txt`):

```txt
sqlalchemy
ttkbootstrap
screeninfo
```

> 💡 Opcional: `psycopg2` si migrás a PostgreSQL  

---

## ▶️ Ejecución

1. Clonar el repositorio  
2. Asegurar dependencias con `pip install -r requirements.txt`  
3. Ejecutar el programa:  

```bash
python Programa_catalogo.py
```

En el primer arranque se pedirá la ruta de la base de datos.  

---

## 🛠️ Arquitectura

- **MVC** puro:
  - `Views/` → Presentación (ventanas y widgets Tkinter)  
  - `Controllers/` → Manejan lógica de flujo e interacción  
  - `Services/` → Reglas de negocio, validaciones, orquestación  
  - `Repositories/` → Acceso a datos mediante SQLAlchemy  
  - `Models/` → Tablas y relaciones ORM  

- **Errores de dominio** centralizados en `custom_errors.py`  
- **Inyección controlada de dependencias**: Controllers crean y enlazan Views + Services.  

---

## 📌 Estado del proyecto

- ✅ Migración completa desde código espagueti a MVC modular  
- ✅ Persistencia desacoplada de lógica de negocio
- 🚧 Próximos pasos:
  - Test unitarios en `pytest` para services y repositories  
  - Añadir las funcionalidades listadas en `TODO.txt`

---

## 👨‍💻 Autor
Proyecto personal en desarrollo como laboratorio de buenas prácticas, patrones de diseño y arquitectura de software.  
Distribución de trabajo sobre **Linux Fedora 42**.  

---
