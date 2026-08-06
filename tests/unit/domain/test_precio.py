from dataclasses import FrozenInstanceError
from decimal import Decimal
import pytest

from app.domain.models.precio import Precio
from app.domain.models.stock import Stock
from app.domain.custom_errors import DomainValidationError, PriceInvalidError


def test_precio_from_string_parses_various_formats():
    assert Precio.from_string("$120,50").value == Decimal("120.50")
    assert Precio.from_string("120,50").value == Decimal("120.50")
    assert Precio.from_string("1.234,56").value == Decimal("1234.56")
    assert Precio.from_string("  $  0,00 ").value == Decimal("0.00")
    assert Precio.from_string("100.25").value == Decimal("100.25")


def test_precio_rejects_negative():
    with pytest.raises(PriceInvalidError):
        Precio(Decimal("-0.01"))
    assert issubclass(PriceInvalidError, DomainValidationError)


def test_precio_str_formatting():
    assert str(Precio(Decimal("0"))) == "$0,00"
    assert str(Precio(Decimal("12.3"))) == "$12,30"
    assert str(Precio(Decimal("1234.56"))) == "$1.234,56"
    assert str(Precio(Decimal("1.999"))) == "$2,00"
    assert str(Precio(Decimal("999.995"))) == "$1.000,00"


def test_precio_from_string_invalid_raises():
    with pytest.raises(PriceInvalidError):
        Precio.from_string("abc")
    with pytest.raises(PriceInvalidError):
        Precio.from_string("   ")


def test_precio_is_immutable_and_type_safe():
    p = Precio(Decimal("50.00"))
    with pytest.raises(FrozenInstanceError):
        p.value = Decimal("60.00")  # type: ignore[misc]

    with pytest.raises(TypeError):
        _ = p + Stock(5)  # type: ignore[operator]

    assert sum([Precio(Decimal("10.00")), Precio(Decimal("15.50"))]) == Precio(Decimal("25.50"))


def test_precio_aplicar_porcentaje():
    p = Precio(Decimal("100.00"))
    assert p.aplicar_porcentaje(Decimal("12.5")) == Precio(Decimal("112.50"))
    assert p.aplicar_porcentaje(Decimal("-50")) == Precio(Decimal("50.00"))
    with pytest.raises(PriceInvalidError):
        p.aplicar_porcentaje(Decimal("-100"))
