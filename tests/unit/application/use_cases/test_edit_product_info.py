import pytest
from decimal import Decimal

from app.application.ports.producto_repository import IProductoRepository, ProductFilter
from app.application.ports.unit_of_work import IUnitOfWork
from app.application.use_cases.edit_product_info import EditProductInfo
from app.domain.models.producto import Producto
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock


class _FakeProductRepo(IProductoRepository):
    def __init__(self):
        self.updated = []

    def save_product(self, product: Producto) -> None:
        pass

    def list_products(self, filtro: ProductFilter | None = None) -> list[Producto]:
        return []

    def count_products(self, filtro: ProductFilter | None = None) -> int:
        return 0

    def get_by_id(self, product_id: int) -> Producto | None:
        return None

    def get_by_barcode(self, barcode: str) -> Producto | None:
        return None

    def get_products_by_id_list(self, ids_buscadas: list[int]) -> list[Producto]:
        return []

    def add_stock(self, id_producto: int, cantidad: int) -> None:
        pass

    def add_stock_to_multiple_products(self, ids_list: list[int], stock_to_add: int) -> None:
        pass

    def set_stock(self, id_producto: int, cantidad: Stock) -> None:
        pass

    def update_all_prices(self, percent_multiplier: Decimal = Decimal("1")) -> None:
        pass

    def update_selected_product_prices(
        self, ids_list: list[int], percent_multiplier: Decimal = Decimal("1")
    ) -> None:
        pass

    def update_price_to_new_value(self, ids_list: list[int], new_price: Precio) -> None:
        pass

    def set_stock_bulk(self, ids_list: list[int], new_stock: Stock) -> None:
        pass

    def update_info_product(self, product: Producto) -> None:
        self.updated.append(product)

    def set_active(self, product_id: int, active: bool) -> bool:
        return True


class _FakeUoW(IUnitOfWork):
    def __init__(self):
        self.product_repo = _FakeProductRepo()
        self.sale_repo = None
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
def test_edit_product_info_updates_repo_and_commits():
    uow_instance = _FakeUoW()

    def factory():
        return uow_instance

    uc = EditProductInfo(factory)

    uc.execute(
        id_producto=5,
        nombre="Paracetamol",
        codigo="PARA500",
        precio="$120,50",
        stock_param="7",
        detalle="Caja x 16",
        codigo_de_barras="7791234567890",
    )

    assert uow_instance.commits == 1
    assert len(uow_instance.product_repo.updated) == 1
    prod = uow_instance.product_repo.updated[0]
    assert prod.id_producto == 5
    assert prod.nombre == "Paracetamol"
    assert isinstance(prod.precio, Precio)
    assert isinstance(prod.stock, Stock)


@pytest.mark.unit
def test_edit_product_info_parses_value_objects():
    uow_instance = _FakeUoW()
    uc = EditProductInfo(lambda: uow_instance)

    uc.execute(
        id_producto=10,
        nombre="Ibuprofeno 400mg",
        codigo="IBU400",
        precio="123,45",
        stock_param="-2",
        detalle="Caja x10",
        codigo_de_barras="7790000000000",
    )

    prod = uow_instance.product_repo.updated[0]
    assert prod.precio.value == Decimal("123.45")
    assert prod.stock.value == -2
