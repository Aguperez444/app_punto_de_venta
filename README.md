# 📦 Catálogo de Productos (Tkinter + SQLAlchemy)

Aplicación de escritorio para la gestión de un catálogo de productos, ventas y stock.  
El proyecto nació como un prototipo **monolítico y acoplado** en `tkinter` + `sqlite3`, y actualmente se encuentra en plena **migración hacia una arquitectura MVC limpia**, con **servicios, controladores y repositorios desacoplados**, utilizando **SQLAlchemy ORM** para la persistencia.

---

## 🚀 Estado del Proyecto
- Versión actual: **Beta 0.1.x**
- **Migración en progreso**: algunas ventanas y casos de uso ya fueron migrados a la nueva estructura (ej. `AddProduct`, `Search`, `SaleRegister`), mientras que otras aún dependen de funciones legacy en `project_functions.py`.  
- En el futuro cercano todo el legacy será eliminado y el proyecto quedará 100% en **MVC + SQLAlchemy**.

---

## 🏗️ Estructura del Proyecto

```bash
APP-MVC-Python-Tkinter-SQLAlchemy/
│
├── Programa_catalogo.py              # Punto de entrada principal
│
├── Views/                            # Interfaz de usuario (Tkinter + ttkbootstrap)
│   ├── main_menu_window.py
│   ├── add_products_window.py
│   ├── search_window.py
│   ├── sale_register_window.py
│   ├── edit_prices_window.py
│   ├── edit_product_info_window.py
│   ├── add_stock_window.py
│   ├── no_stock_list_window.py
│   ├── view_sales_window.py
│   └── base_window_toplevel.py       # Clases base para ventanas comunes
│
├── Controllers/                      # Controladores (coordinan vista ↔ servicio)
│   ├── program_start_controller.py
│   ├── common_window_innit_controller.py
│   ├── add_product_controller.py
│   ├── find_product_controller.py
│   └── register_sale_controller.py
│
├── Services/                         # Lógica de negocio
│   ├── ProductoService.py
│   ├── VentaService.py
│   └── DetalleService.py
│
├── Models/                           # Entidades de dominio (SQLAlchemy ORM)
│   ├── Producto.py
│   ├── Venta.py
│   └── DetalleVenta.py
│
├── Database/                      # Repositorios y gestión de persistencia
│   └── db_session.py (y otros repositorios)
│
├── ZOLD/                             # Código legado en proceso de eliminación
│
└── project_functions.py              # Legacy utils (será eliminado al final)
```

---

## ⚙️ Tecnologías

- **Python 3.13**
- **Tkinter** + [ttkbootstrap](https://ttkbootstrap.readthedocs.io/en/latest/)  
- **SQLAlchemy ORM** para persistencia
- **SQLite** (por ahora, con posibilidad de migrar a PostgreSQL)
- **MVC + GRASP** como guías de arquitectura

---

## ✨ Funcionalidades Actuales

- 📋 **Gestión de productos**: alta, baja, modificación, búsqueda por nombre/código/barras.  
- 💲 **Edición de precios**: actualización masiva o individual con incrementos porcentuales o valores manuales.  
- 📦 **Gestión de stock**: añadir stock, ver productos sin stock.  
- 🛒 **Registro de ventas**: con detalles y actualización automática del stock.  
- 📊 **Listado de ventas**: por día o mes, con cálculo de totales.  
- 🎨 **UI moderna** con temas claro/oscuro (ttkbootstrap).  

---

## 🔄 Proceso de Migración

1. **Antes**:  
   - Lógica mezclada en las views.  
   - Acceso directo a SQLite con `sqlite3`.  
   - Funciones globales en `project_functions.py`.

2. **Ahora**:  
   - Separación clara en **MVC**:
     - `Views` → interfaz Tkinter.  
     - `Controllers` → coordinan eventos y validaciones.  
     - `Services` → reglas de negocio.  
     - `Persistence/Repository` → acceso a BD vía SQLAlchemy.  
   - Modelos en SQLAlchemy (`Producto`, `Venta`, `DetalleVenta`).  
   - Migración progresiva de cada ventana a esta nueva arquitectura.  

3. **Futuro**:
   - Eliminar por completo `project_functions.py` y `ZOLD/`.  
   - Completar repositorios SQLAlchemy para todas las entidades.  
   - Considerar migración de backend a PostgreSQL.  
   - Eventual port a interfaz web.  

---

## 🖼️ Capturas

*(pendiente de añadir screenshots de la UI con ttkbootstrap)*

---

## 👨‍💻 Autor
Proyecto personal en desarrollo como laboratorio de buenas prácticas, patrones de diseño y arquitectura de software.  
Distribución de trabajo sobre **Linux Fedora 42**.  

---
