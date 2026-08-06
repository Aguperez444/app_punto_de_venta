from dataclasses import FrozenInstanceError
from decimal import Decimal
import pytest

from app.domain.models.precio import Precio
from app.domain.models.stock import Stock
from app.domain.custom_errors import DomainValidationError, StockInvalidError


def test_stock_from_string_parses_int_including_negative():
    assert Stock.from_string("15").value == 15
    assert Stock.from_string("  -3 ").value == -3
    assert Stock(-5).value == -5


def test_stock_from_string_invalid_raises():
    assert issubclass(StockInvalidError, DomainValidationError)
    with pytest.raises(StockInvalidError):
        Stock.from_string("1.5")
    with pytest.raises(StockInvalidError):
        Stock.from_string("abc")
    with pytest.raises(StockInvalidError):
        Stock(True)  # type: ignore[arg-type]


def test_stock_str():
    assert str(Stock(0)) == "0"
    assert str(Stock(12)) == "12"
    assert str(Stock(-2)) == "-2"


def test_stock_is_immutable_and_supports_negative_arithmetic():
    s = Stock(2)
    with pytest.raises(FrozenInstanceError):
        s.value = 10  # type: ignore[misc]

    assert s - Stock(5) == Stock(-3)
    assert s + 3 == Stock(5)
    with pytest.raises(TypeError):
        _ = s + Precio(Decimal("10"))  # type: ignore[operator]
