import pytest
from datetime import datetime, timedelta

from app.application.use_cases.query_sales import QuerySales


class _FakeSaleRepo:
    def __init__(self, result=None):
        self.calls = []
        self.result = result or []

    def find_ventas_by_date(self, start, end):
        self.calls.append((start, end))
        return list(self.result)


class _FakeUoW:
    def __init__(self, sale_repo):
        self.product_repo = None
        self.sale_repo = sale_repo

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _factory(uow):
    return lambda: uow


@pytest.mark.unit
def test_by_date_uses_start_of_day_and_next_day():
    sale_repo = _FakeSaleRepo([])
    uow = _FakeUoW(sale_repo)
    uc = QuerySales(_factory(uow))

    date = datetime(2025, 10, 14, 18, 26)
    uc.by_date(date)

    assert len(sale_repo.calls) == 1
    start, end = sale_repo.calls[0]
    assert start == datetime(2025, 10, 14, 0, 0, 0)
    assert end == start + timedelta(days=1)


@pytest.mark.unit
def test_by_range_passes_dates_through():
    sale_repo = _FakeSaleRepo([])
    uow = _FakeUoW(sale_repo)
    uc = QuerySales(_factory(uow))

    start = datetime(2025, 1, 1)
    end = datetime(2025, 1, 31)
    uc.by_range(start, end)

    assert sale_repo.calls == [(start, end)]


@pytest.mark.unit
def test_by_month_builds_correct_range():
    sale_repo = _FakeSaleRepo([])
    uow = _FakeUoW(sale_repo)
    uc = QuerySales(_factory(uow))

    uc.by_month(2024, 12)

    start, end = sale_repo.calls[0]
    assert start == datetime(2024, 12, 1)
    assert end == datetime(2025, 1, 1)
