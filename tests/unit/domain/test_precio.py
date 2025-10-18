from decimal import Decimal
import pytest
from app.domain.models.precio import Precio
from app.domain.custom_errors import PriceInvalidError


def test_precio_from_string_parses_various_formats():
    assert Precio.from_string("$120,50").value == Decimal("120.50")
    assert Precio.from_string("120,50").value == Decimal("120.50")
    assert Precio.from_string("1.234,56").value == Decimal("1234.56")
    assert Precio.from_string("  $  0,00 ").value == Decimal("0.00")


def test_precio_rejects_negative():
    with pytest.raises(PriceInvalidError):
        Precio(Decimal("-0.01"))


def test_precio_str_formatting():
    assert str(Precio(Decimal("0"))) == "$0,00"
    assert str(Precio(Decimal("12.3"))) == "$12,30"
    assert str(Precio(Decimal("1234.56"))) == "$1.234,56"


def test_precio_from_string_invalid_raises():
    with pytest.raises(PriceInvalidError):
        Precio.from_string("abc")
