import pytest

from app.application.use_cases.edit_stock import EditStock


class _FakeProductRepo:
    def __init__(self):
        self.add_calls = []
        self.set_calls = []
        self.set_bulk_calls = []

    def add_stock(self, product_id: int, cantidad: int) -> None:
        self.add_calls.append((product_id, cantidad))

    def set_stock(self, product_id: int, stock_obj) -> None:
        # accept Stock object
        self.set_calls.append((product_id, stock_obj.value))

    def set_stock_bulk(self, ids_list, stock_obj) -> None:
        self.set_bulk_calls.append((list(ids_list), stock_obj.value))


class _FakeUoW:
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


def _factory(uow):
    return lambda: uow


@pytest.mark.unit
def test_add_stock_calls_repo_and_commits():
    uow = _FakeUoW()
    uc = EditStock(_factory(uow))

    uc.add_stock(id_producto=1, cantidad=5)

    assert uow.commits >= 1
    assert uow.product_repo.add_calls == [(1, 5)]


@pytest.mark.unit
def test_set_stock_wraps_in_value_object_and_commits():
    uow = _FakeUoW()
    uc = EditStock(_factory(uow))

    uc.set_stock(id_producto=2, cantidad=7)

    assert uow.commits >= 1
    assert uow.product_repo.set_calls == [(2, 7)]


@pytest.mark.unit
def test_set_stock_bulk_handles_empty_list():
    uow = _FakeUoW()
    uc = EditStock(_factory(uow))

    assert uc.set_stock_bulk([], 9) is None
    assert uow.commits == 0
    assert uow.product_repo.set_bulk_calls == []


@pytest.mark.unit
def test_set_stock_bulk_calls_repo_and_commits():
    uow = _FakeUoW()
    uc = EditStock(_factory(uow))

    uc.set_stock_bulk([1, 2, 3], 11)

    assert uow.commits >= 1
    assert uow.product_repo.set_bulk_calls == [([1, 2, 3], 11)]
