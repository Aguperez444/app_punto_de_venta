import pytest
from decimal import Decimal
from app.domain.models.producto import Producto
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock


def test_producto_from_string_creates_value_objects():
    p = Producto.from_string(
        nombre="Paracetamol",
        codigo="PARA500",
        precio_param="$1.234,56",
        detalle="Caja x 16",
        codigo_de_barras="7791234567890",
        stock_param="20",
    )
    assert p.nombre == "Paracetamol"
    assert p.codigo == "PARA500"
    assert isinstance(p.precio, Precio)
    assert p.precio.value == Decimal("1234.56")
    assert isinstance(p.stock, Stock)
    assert p.stock.value == 20


def test_producto_disminuir_stock_success(sample_producto):
    sample_producto.disminuir_stock(3)
    assert sample_producto.stock.value == 7


def test_producto_disminuir_stock_rejects_negative_amount(sample_producto):
    with pytest.raises(ValueError):
        sample_producto.disminuir_stock(-1)
