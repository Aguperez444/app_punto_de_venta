from decimal import Decimal
import pytest

from app.application.services.sale_cart import SaleCart
from app.application.use_cases.register_sale import RegisterSale, SaleItemInput
from app.domain.custom_errors import EmptySaleError, NotFoundProductError
from app.domain.models.precio import Precio
from app.domain.models.producto import Producto
from app.domain.models.stock import Stock


class _MultiProductRepo:
    def __init__(self, products: list[Producto]):
        self._products = {p.id_producto: p for p in products}
        self.stock_updates: list[tuple[int, int]] = []

    def get_by_id(self, product_id: int) -> Producto | None:
        return self._products.get(product_id)

    def set_stock(self, product_id: int, stock: Stock) -> None:
        self.stock_updates.append((product_id, stock.value))


class _FakeSaleRepo:
    def __init__(self):
        self.saved = []

    def save_new(self, venta):
        venta.id_venta = len(self.saved) + 1
        self.saved.append(venta)


class _FakeUoW:
    def __init__(self, products: list[Producto]):
        self.product_repo = _MultiProductRepo(products)
        self.sale_repo = _FakeSaleRepo()
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
def test_sale_cart_add_merge_update_remove_and_totals():
    p1 = Producto(1, "Ibuprofeno", "IBU", Precio(Decimal("120.50")), "", "7791", Stock(2))
    p2 = Producto(2, "Jarabe", "JAR", Precio(Decimal("350.00")), "", "7792", Stock(0))

    cart = SaleCart()
    assert cart.is_empty is True
    assert cart.has_items is False
    assert str(cart.total) == "$0,00"

    cart.add_item(p1, 2)
    assert cart.has_items is True
    assert cart.items_count == 1
    assert cart.total_units == 2
    assert cart.total == Precio(Decimal("241.00"))

    # Agregar el mismo producto acumula cantidad
    cart.add_item(p1, 1)
    assert cart.items_count == 1
    assert cart.total_units == 3
    assert cart.total == Precio(Decimal("361.50"))

    cart.add_item(p2, 1)
    assert cart.items_count == 2
    assert cart.total_units == 4
    assert cart.total == Precio(Decimal("711.50"))

    cart.update_quantity(1, 2)
    assert cart.total == Precio(Decimal("591.00"))

    cart.update_quantity(2, 0)
    assert cart.items_count == 1

    cart.remove_item(1)
    assert cart.is_empty is True


@pytest.mark.unit
def test_register_sale_execute_cart_atomic_and_allows_negative_stock():
    p1 = Producto(1, "Ibuprofeno", "IBU", Precio(Decimal("100.00")), "", "7791", Stock(1))
    p2 = Producto(2, "Paracetamol", "PAR", Precio(Decimal("50.00")), "", "7792", Stock(0))
    uow = _FakeUoW([p1, p2])

    uc = RegisterSale(lambda: uow)
    sale_id = uc.execute_cart(
        [
            SaleItemInput(product_id=1, amount=3),
            SaleItemInput(product_id=2, amount=2),
            SaleItemInput(product_id=1, amount=1),  # repetido: suma 4 total
        ]
    )

    assert sale_id == 1
    assert uow.commits == 1
    assert p1.stock.value == -3  # 1 - 4 = -3 (permitido por regla de negocio)
    assert p2.stock.value == -2  # 0 - 2 = -2
    assert len(uow.sale_repo.saved) == 1
    venta = uow.sale_repo.saved[0]
    assert venta.total_price == Precio(Decimal("500.00"))
    assert len(venta.detalles) == 2


@pytest.mark.unit
def test_register_sale_execute_cart_validates_empty_and_missing_product():
    p1 = Producto(1, "Ibuprofeno", "IBU", Precio(Decimal("100.00")), "", "7791", Stock(5))
    uow = _FakeUoW([p1])
    uc = RegisterSale(lambda: uow)

    with pytest.raises(EmptySaleError):
        uc.execute_cart([])

    with pytest.raises(NotFoundProductError):
        uc.execute_cart([SaleItemInput(1, 2), SaleItemInput(999, 1)])

    # Atomicidad: si falta un producto, no se descuenta stock ni se hace commit
    assert p1.stock.value == 5
    assert uow.commits == 0
