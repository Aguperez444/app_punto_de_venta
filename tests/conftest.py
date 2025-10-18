import sys
from types import SimpleNamespace
from decimal import Decimal
import pytest
from faker import Faker

from app.domain.models.precio import Precio
from app.domain.models.stock import Stock
from app.domain.models.producto import Producto


@pytest.fixture(scope="session")
def faker() -> Faker:
    return Faker("es_AR")


@pytest.fixture()
def sample_precio() -> Precio:
    return Precio(Decimal("123.45"))


@pytest.fixture()
def sample_stock() -> Stock:
    return Stock(10)


@pytest.fixture()
def sample_producto(sample_precio: Precio, sample_stock: Stock) -> Producto:
    return Producto(
        id_producto=None,
        nombre="Ibuprofeno 400mg",
        codigo="IBU400",
        precio=sample_precio,
        detalle="Caja x 10 comprimidos",
        codigo_de_barras="7790000000000",
        stock=sample_stock,
    )


class FakeProductRepo:
    def __init__(self, product: Producto | None = None):
        self.saved_products = []
        self.updated_products = []
        self._product = product

    # Used by AddProduct
    def save_product(self, product: Producto) -> None:
        self.saved_products.append(product)
        # simulate DB assigning an ID
        if product.id_producto is None:
            product.id_producto = 1

    # Used by RegisterSale
    def get_by_id(self, product_id: int) -> Producto | None:
        return self._product

    def update_info_product(self, product: Producto) -> None:
        self.updated_products.append(product)


class FakeSaleRepo:
    def __init__(self):
        self.saved_sales = []

    def save_new(self, venta):
        # simulate DB assigning an ID to sale and its details if needed
        venta.id_venta = 1
        self.saved_sales.append(venta)


class FakeUoW:
    def __init__(self, product=None):
        self.product_repo = FakeProductRepo(product)
        self.sale_repo = FakeSaleRepo()
        self._entered = False
        self.commits = 0
        self.rollbacks = 0

    def __enter__(self):
        self._entered = True
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.commits += 1
        else:
            self.rollbacks += 1
        return False  # don't suppress exceptions

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


@pytest.fixture()
def fake_uow_factory():
    # returns a callable that builds a new FakeUoW (without preloaded product)
    def factory():
        return FakeUoW()
    return factory


@pytest.fixture()
def fake_uow_factory_with_product(sample_producto: Producto):
    def factory():
        return FakeUoW(product=sample_producto)
    return factory
