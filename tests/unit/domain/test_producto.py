import pytest
from decimal import Decimal

from app.domain.custom_errors import DomainValidationError
from app.domain.models.producto import Producto
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock


def test_producto_from_string_creates_value_objects():
    p = Producto.from_string(
        nombre="  Paracetamol  ",
        codigo=" PARA500 ",
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
    assert p.activo is True


def test_producto_rejects_blank_nombre_or_codigo():
    with pytest.raises(DomainValidationError):
        Producto.from_string("   ", "COD", "10", "", "", "1")
    with pytest.raises(DomainValidationError):
        Producto.from_string("Prod", "   ", "10", "", "", "1")


def test_producto_allows_optional_detalle_and_barcode():
    p = Producto.from_string("Aspirina", "ASP100", "50,00", None, None, "0")
    assert p.detalle == ""
    assert p.codigo_de_barras == ""


def test_producto_disminuir_stock_success_and_allows_negative(sample_producto):
    sample_producto.disminuir_stock(3)
    assert sample_producto.stock.value == 7

    # Regla de negocio: el stock puede quedar negativo al vender antes de cargar stock
    sample_producto.disminuir_stock(12)
    assert sample_producto.stock.value == -5


def test_producto_ajustar_stock_and_soft_delete(sample_producto):
    sample_producto.ajustar_stock(-15)
    assert sample_producto.stock.value == -5
    sample_producto.ajustar_stock(10)
    assert sample_producto.stock.value == 5

    sample_producto.desactivar()
    assert sample_producto.activo is False
    sample_producto.reactivar()
    assert sample_producto.activo is True


def test_producto_disminuir_stock_rejects_negative_amount(sample_producto):
    with pytest.raises(ValueError):
        sample_producto.disminuir_stock(-1)


def test_producto_from_persistence_allows_legacy_blank_fields():
    legacy = Producto.from_persistence(
        id_producto=99,
        nombre="",
        codigo="   ",
        precio=Precio(Decimal("10.00")),
        detalle=None,
        codigo_de_barras=None,
        stock=Stock(0),
        activo=True,
    )
    assert legacy.id_producto == 99
    assert legacy.nombre == ""
    assert legacy.codigo == ""
