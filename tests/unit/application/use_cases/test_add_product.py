import pytest

from app.application.use_cases.add_product import AddProduct
from app.domain.custom_errors import DomainValidationError


@pytest.mark.unit
def test_add_product_saves_and_assigns_id(fake_uow_factory):
    uc = AddProduct(fake_uow_factory)
    producto = uc.execute(
        nombre="Amoxicilina",
        codigo="AMOX500",
        precio_param="$123,45",
        detalle="Caja x 12",
        codigo_de_barras="7791111111111",
        stock_param="5",
    )
    assert producto.id_producto == 1
    assert producto.nombre == "Amoxicilina"


@pytest.mark.unit
def test_add_product_invalid_price_raises(fake_uow_factory):
    uc = AddProduct(fake_uow_factory)
    with pytest.raises(Exception):
        uc.execute(
            nombre="X",
            codigo="X",
            precio_param="abc",
            detalle="",
            codigo_de_barras="",
            stock_param="1",
        )
