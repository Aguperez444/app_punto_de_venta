import pytest
from app.domain.models.stock import Stock
from app.domain.custom_errors import StockInvalidError


def test_stock_from_string_parses_int():
    assert Stock.from_string("15").value == 15


def test_stock_from_string_invalid_raises():
    with pytest.raises(StockInvalidError):
        Stock.from_string("1.5")
    with pytest.raises(StockInvalidError):
        Stock.from_string("abc")


def test_stock_str():
    assert str(Stock(0)) == "0"
    assert str(Stock(12)) == "12"
