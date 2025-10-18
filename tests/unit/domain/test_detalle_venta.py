from decimal import Decimal
import pytest

from app.domain.custom_errors import PriceInvalidError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.precio import Precio


def test_detalle_venta_create_new_and_subtotal_rounding():
    det = DetalleVenta.create_new(producto_id=10, cantidad=3, precio_unitario=Precio(Decimal("12.345")))
    # subtotal = 3 * 12.345 = 37.035 -> round to two decimals in code => 37.03
    assert det.cantidad == 3
    assert det.producto_id == 10
    assert det.precio_unitario_actual.value == Decimal("12.345")
    assert det.calcular_subtotal() == Decimal("37.04")


def test_detalle_venta_invalid_quantity():
    with pytest.raises(ValueError):
        DetalleVenta.create_new(producto_id=1, cantidad=0, precio_unitario=Precio(Decimal("10")))


def test_detalle_venta_invalid_price():
    with pytest.raises(PriceInvalidError):
        DetalleVenta.create_new(producto_id=1, cantidad=1, precio_unitario=Precio(Decimal("-1")))
