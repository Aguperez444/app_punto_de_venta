from freezegun import freeze_time
import pytest

from app.application.use_cases.register_sale import RegisterSale
from app.domain.custom_errors import NotFoundProductError


@pytest.mark.unit
def test_register_sale_success(fake_uow_factory_with_product):
    uc = RegisterSale(fake_uow_factory_with_product)

    with freeze_time("2025-03-10 15:30:00"):
        sale_id = uc.execute(product_id=1, amount=2)

    assert sale_id == 1


@pytest.mark.unit
def test_register_sale_decreases_stock_and_commits(fake_uow_factory_with_product, sample_producto):
    initial = sample_producto.stock.value
    uc = RegisterSale(fake_uow_factory_with_product)

    sale_id = uc.execute(product_id=1, amount=3)

    assert sample_producto.stock.value == initial - 3
    assert sale_id == 1


@pytest.mark.unit
def test_register_sale_not_found_raises(fake_uow_factory_with_product):
    uc = RegisterSale(fake_uow_factory_with_product)
    with pytest.raises(NotFoundProductError):
        uc.execute(product_id=999, amount=1)
