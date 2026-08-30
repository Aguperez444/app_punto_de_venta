from datetime import datetime
from decimal import Decimal
import pytest

from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.precio import Precio
from app.domain.models.producto import Producto
from app.domain.models.stock import Stock
from app.domain.models.venta import Venta
from app.infrastructure.ui.tkinter.controllers.actions.add_product_controller import (
    AddProductController,
)
from app.infrastructure.ui.tkinter.controllers.actions.edit_product_info_controller import (
    EditProductInfoController,
)
from app.infrastructure.ui.tkinter.controllers.actions.show_product_controller import (
    ShowProductController,
)
from app.infrastructure.ui.tkinter.controllers.actions.show_sales_controller import (
    ShowSalesController,
)


class _DummyView:
    def __init__(self):
        self.container = None
        self.errors = []
        self.messages = []
        self.rows = []
        self.cleaned = 0
        self.cart_updates = []
        self.sales_rows = []
        self.total_shown = None
        self.rendered = False

    def render_view(self):
        self.rendered = True

    def show_error(self, msg):
        self.errors.append(msg)

    def show_error_message(self, msg):
        self.errors.append(msg)

    def show_message(self, msg):
        self.messages.append(msg)

    def show_success_message(self):
        self.messages.append("ok")

    def pasar_al_cuadro(self, products):
        self.rows = list(products)

    def clean_treeview(self):
        self.rows = []
        self.cleaned += 1

    def update_cart_summary(self, items_count, total_units, total_str):
        self.cart_updates.append((items_count, total_units, total_str))

    def realizar_busqueda(self):
        pass

    def pasar_al_cuadro_ventas(self, summaries):
        self.sales_rows = list(summaries)

    def mostrar_total_ventas(self, total_str):
        self.total_shown = total_str


class _InMemoryRepo:
    def __init__(self):
        self.products: dict[int, Producto] = {}
        self.sales: list[Venta] = []
        self._next_pid = 1

    def save_product(self, product: Producto):
        product.id_producto = self._next_pid
        self._next_pid += 1
        self.products[product.id_producto] = product

    def get_by_id(self, pid: int):
        return self.products.get(pid)

    def set_stock(self, pid: int, stock: Stock):
        p = self.products[pid]
        p._stock = stock

    def set_active(self, pid: int, active: bool):
        if pid not in self.products:
            return False
        if active:
            self.products[pid].reactivar()
        else:
            self.products[pid].desactivar()
        return True

    def save_new(self, venta: Venta):
        venta.id_venta = len(self.sales) + 1
        self.sales.append(venta)

    def find_ventas_by_date(self, start, end):
        return list(self.sales)


class _InMemoryUoW:
    def __init__(self, repo: _InMemoryRepo):
        self.product_repo = repo
        self.sale_repo = repo
        self.commits = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def commit(self):
        self.commits += 1

    def rollback(self):
        pass


@pytest.mark.unit
def test_add_product_controller_allows_optional_fields_and_validates_required():
    repo = _InMemoryRepo()
    view = _DummyView()
    ctrl = AddProductController(view, uow_factory_param=lambda: _InMemoryUoW(repo))

    # Falta campo obligatorio 'codigo'
    ok = ctrl.add_product(
        {"nombre": "Aspirina", "codigo": "", "precio": "$100,00", "stock": "5", "detalle": "", "codigo_de_barras": ""}
    )
    assert ok is False
    assert len(view.errors) == 1

    # Campos opcionales vacíos permitidos
    ok = ctrl.add_product(
        {"nombre": "Aspirina", "codigo": "ASP", "precio": "$100,00", "stock": "5", "detalle": "", "codigo_de_barras": ""}
    )
    assert ok is True
    assert len(repo.products) == 1


@pytest.mark.unit
def test_show_product_controller_cart_checkout_flow():
    repo = _InMemoryRepo()
    p1 = Producto(1, "Ibuprofeno", "IBU", Precio(Decimal("100.00")), "", "7791", Stock(1))
    p2 = Producto(2, "Jarabe", "JAR", Precio(Decimal("250.00")), "", "7792", Stock(0))
    repo.products = {1: p1, 2: p2}

    view = _DummyView()
    ctrl = ShowProductController(view, uow_factory_param=lambda: _InMemoryUoW(repo))

    assert ctrl.cart.is_empty is True
    ctrl.add_product_to_cart(p1, 2)
    ctrl.add_product_to_cart(p2, 1)

    assert ctrl.cart.has_items is True
    assert view.cart_updates[-1] == (2, 3, "$450,00")

    confirmed = ctrl.confirm_cart_sale()
    assert confirmed is True
    assert ctrl.cart.is_empty is True
    assert len(repo.sales) == 1
    assert repo.products[1].stock.value == -1
    assert repo.products[2].stock.value == -1


@pytest.mark.unit
def test_edit_product_info_controller_delete_and_restore():
    repo = _InMemoryRepo()
    p = Producto(1, "Crema", "CRM", Precio(Decimal("500.00")), "", "", Stock(3))
    repo.products = {1: p}

    view = _DummyView()
    ctrl = EditProductInfoController(view, uow_factory_param=lambda: _InMemoryUoW(repo))

    assert ctrl.delete_product(1) is True
    assert p.activo is False
    assert ctrl.restore_product(1) is True
    assert p.activo is True


@pytest.mark.unit
def test_show_sales_controller_presents_dtos_and_exports_csv(tmp_path):
    repo = _InMemoryRepo()
    p = Producto(1, "Vitamina C", "VIT", Precio(Decimal("80.00")), "", "", Stock(10))
    venta = Venta.nueva(datetime(2026, 8, 22, 10, 0, 0))
    venta.id_venta = 1
    venta.agregar_detalle(DetalleVenta(1, 1, 1, 2, p.precio, product=p))
    repo.sales.append(venta)

    view = _DummyView()
    ctrl = ShowSalesController(view, uow_factory_param=lambda: _InMemoryUoW(repo))
    ctrl.get_ventas_del_dia(datetime(2026, 8, 22))

    assert len(view.sales_rows) == 1
    assert view.sales_rows[0].resumen_productos == "Vitamina C"
    assert view.total_shown == "$160,00"

    csv_file = tmp_path / "ventas_ctrl.csv"
    assert ctrl.export_current_sales_to_csv(str(csv_file)) is True
    assert csv_file.exists()


@pytest.mark.unit
def test_sales_date_navigation_helpers():
    from app.infrastructure.ui.tkinter.views.views.show_sales_list_view import (
        shift_date_by_days,
        shift_date_by_months,
    )

    # Días
    assert shift_date_by_days(datetime(2026, 8, 1), -1) == datetime(2026, 7, 31)
    assert shift_date_by_days(datetime(2026, 8, 31), 1) == datetime(2026, 9, 1)

    # Meses (cambio de año y ajuste de fin de mes)
    assert shift_date_by_months(datetime(2026, 1, 15), -1) == datetime(2025, 12, 15)
    assert shift_date_by_months(datetime(2026, 12, 15), 1) == datetime(2027, 1, 15)
    assert shift_date_by_months(datetime(2026, 3, 31), -1) == datetime(2026, 2, 28)
    assert shift_date_by_months(datetime(2024, 3, 31), -1) == datetime(2024, 2, 29)
