import pytest

from app.application.use_cases.update_price import UpdatePrice


class _FakeProductRepo:
    def __init__(self):
        self.update_all_calls = []
        self.update_selected_calls = []
        self.update_to_value_calls = []

    def update_all_prices(self, multiplier: float):
        self.update_all_calls.append(multiplier)

    def update_selected_product_prices(self, ids_list, multiplier: float):
        self.update_selected_calls.append((list(ids_list), multiplier))

    def update_price_to_new_value(self, ids_list, new_price):
        # new_price is Precio
        self.update_to_value_calls.append((list(ids_list), new_price.value))


class _FakeUoW:
    def __init__(self):
        self.product_repo = _FakeProductRepo()
        self.sale_repo = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _factory(uow):
    return lambda: uow


@pytest.mark.unit
def test_update_all_parses_percent_and_calls_repo():
    uow = _FakeUoW()
    uc = UpdatePrice(_factory(uow))

    uc.update_all(10)  # +10% => 1.1

    assert uow.product_repo.update_all_calls == [1.1]


@pytest.mark.unit
def test_update_all_invalid_percent_raises():
    uow = _FakeUoW()
    uc = UpdatePrice(_factory(uow))

    with pytest.raises(ValueError):
        uc.update_all("abc")


@pytest.mark.unit
def test_update_selected_handles_empty_ids():
    uow = _FakeUoW()
    uc = UpdatePrice(_factory(uow))

    assert uc.update_selected([], 5) is None
    assert uow.product_repo.update_selected_calls == []


@pytest.mark.unit
def test_update_selected_raises_on_zero_multiplier():
    uow = _FakeUoW()
    uc = UpdatePrice(_factory(uow))

    with pytest.raises(ValueError):
        uc.update_selected([1], -100.0)


@pytest.mark.unit
def test_update_selected_calls_repo():
    uow = _FakeUoW()
    uc = UpdatePrice(_factory(uow))

    uc.update_selected([1, 2], 5.0)

    assert uow.product_repo.update_selected_calls == [([1, 2], 1.05)]


@pytest.mark.unit
def test_update_to_new_value_wraps_precio():
    uow = _FakeUoW()
    uc = UpdatePrice(_factory(uow))

    uc.update_to_new_value([3, 4], "$12,34")

    assert len(uow.product_repo.update_to_value_calls) == 1
    ids, price_value = uow.product_repo.update_to_value_calls[0]
    assert ids == [3, 4]
    assert float(price_value) == 12.34
