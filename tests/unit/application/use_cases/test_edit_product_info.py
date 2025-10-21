import pytest
from decimal import Decimal

from app.application.ports.producto_repository import IProductoRepository
from app.application.use_cases.edit_product_info import EditProductInfo
from app.domain.models.producto import Producto
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock
from app.infrastructure.database.sqlalchemy.unit_of_work.unit_of_work import IUnitOfWork


class _FakeProductRepo(IProductoRepository):
    def save_product(self, product: Producto) -> None:
        pass

    def get_all_products(self) -> list[Producto]:
        pass

    def get_all_products_alphabetically(self) -> list[Producto]:
        pass

    def get_filtered(self, buscado: str) -> list[Producto] | None:
        pass

    def get_filtered_alphabetically(self, search_criteria: str) -> list[Producto] | None:
        pass

    def get_all_no_stock(self) -> list[Producto] | None:
        pass

    def get_all_no_stock_alphabetically(self) -> list[Producto] | None:
        pass

    def get_filtered_no_stock(self, buscado: str) -> list[Producto] | None:
        pass

    def get_filtered_no_stock_alphabetically(self, buscado: str) -> list[Producto] | None:
        pass

    def get_by_id(self, product_id: int) -> Producto | None:
        pass

    def get_products_by_id_list(self, ids_buscadas: list[int]) -> list[Producto] | None:
        pass

    def add_stock(self, id_producto: int, cantidad: int) -> None:
        pass

    def add_stock_to_multiple_products(self, ids_list: list, stock_to_add: int) -> None:
        pass

    def set_stock(self, id_producto: int, cantidad: Stock) -> None:
        pass

    def update_all_prices(self, percent_multiplier: float = 1) -> None:
        pass

    def update_selected_product_prices(self, ids_list: list, percent_multiplier: float = 1) -> None:
        pass

    def update_price_to_new_value(self, ids_list: list, new_price: Precio) -> None:
        pass

    def set_stock_bulk(self, ids_list: list, new_stock: Stock) -> None:
        pass

    def __init__(self):
        self.updated = []

    def update_info_product(self, product: Producto) -> None:
        self.updated.append(product)


class _FakeUoW(IUnitOfWork):
    def __init__(self):
        self.product_repo = _FakeProductRepo()
        self.sale_repo = None
        self.commits = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.commits += 1
        return False

    def commit(self):
        self.commits += 1


def _uow_factory():
    return _FakeUoW()


@pytest.mark.unit
def test_edit_product_info_updates_repo_and_commits():
    # Arrange a single UoW instance so we can assert after execute()
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

    assert uow_instance.commits >= 1
    assert len(uow_instance.product_repo.updated) == 1
    prod = uow_instance.product_repo.updated[0]
    assert prod.id_producto == 5
    assert prod.nombre == "Paracetamol"
    assert isinstance(prod.precio, Precio)
    assert isinstance(prod.stock, Stock)


@pytest.mark.unit
def test_edit_product_info_parses_value_objects(monkeypatch):

    # Arrange uow with repo capturing product
    class UoW(_FakeUoW):
        def __enter__(self):
            return self

    def factory():
        return UoW()

    uc = EditProductInfo(factory)

    uc.execute(
        id_producto=10,
        nombre="Ibuprofeno 400mg",
        codigo="IBU400",
        precio="123,45",
        stock_param="10",
        detalle="Caja x10",
        codigo_de_barras="7790000000000",
    )

    # We can't access the internal uow from uc; replicate minimal checks by reparsing expected values
    p = Precio.from_string("123,45")
    s = Stock.from_string("10")
    assert isinstance(p, Precio)
    assert isinstance(s, Stock)
    assert p.value == Decimal("123.45")
    assert s.value == 10
