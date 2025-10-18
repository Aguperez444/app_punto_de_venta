import pytest

from app.application.use_cases.query_products import QueryProducts
from app.domain.models.producto import Producto
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock


class _FakeProductRepo:
    def __init__(self, products=None):
        self.products = products or []
        self.by_id = {}
        for p in self.products:
            self.by_id[p.id_producto] = p

    def get_all_products(self):
        return list(self.products)

    def get_all_products_alphabetically(self):
        return sorted(self.products, key=lambda p: p.nombre)

    def get_by_id(self, product_id: int):
        return self.by_id.get(product_id)


class _FakeUoW:
    def __init__(self, repo):
        self.product_repo = repo
        self.sale_repo = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _factory(uow):
    return lambda: uow


@pytest.mark.unit
def test_get_all_returns_products():
    prods = [
        Producto(1, "B", "B1", Precio.from_string("10"), "", "1", Stock.from_string("1")),
        Producto(2, "A", "A1", Precio.from_string("20"), "", "2", Stock.from_string("2")),
    ]
    repo = _FakeProductRepo(prods)
    uow = _FakeUoW(repo)
    uc = QueryProducts(_factory(uow))

    result = uc.get_all()

    assert [p.id_producto for p in result] == [1, 2]


@pytest.mark.unit
def test_get_all_alphabetically_sorts_by_name():
    prods = [
        Producto(1, "B", "B1", Precio.from_string("10"), "", "1", Stock.from_string("1")),
        Producto(2, "A", "A1", Precio.from_string("20"), "", "2", Stock.from_string("2")),
    ]
    repo = _FakeProductRepo(prods)
    uow = _FakeUoW(repo)
    uc = QueryProducts(_factory(uow))

    result = uc.get_all_alphabetically()

    assert [p.nombre for p in result] == ["A", "B"]


@pytest.mark.unit
def test_get_product_name_by_id_returns_empty_when_not_found():
    repo = _FakeProductRepo([])
    uow = _FakeUoW(repo)
    uc = QueryProducts(_factory(uow))

    assert uc.get_product_name_by_id(999) == ""


@pytest.mark.unit
def test_get_product_name_by_id_returns_name():
    p = Producto(5, "Vitamina C", "VITC", Precio.from_string("30"), "", "5", Stock.from_string("3"))
    repo = _FakeProductRepo([p])
    uow = _FakeUoW(repo)
    uc = QueryProducts(_factory(uow))

    assert uc.get_product_name_by_id(5) == "Vitamina C"
