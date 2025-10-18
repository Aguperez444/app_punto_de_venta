import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from app.application.use_cases.add_product import AddProduct
from app.application.use_cases.edit_product_info import EditProductInfo
from app.application.use_cases.edit_stock import EditStock
from app.application.use_cases.update_price import UpdatePrice
from app.application.use_cases.register_sale import RegisterSale
from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.query_sales import QuerySales


pytestmark = pytest.mark.integration


def create_product(uow_factory, nombre="Prod A", codigo="PA", precio="100.00", detalle="", cod_barras="", stock="5"):
    add_uc = AddProduct(uow_factory)
    return add_uc.execute(nombre, codigo, precio, detalle, cod_barras, stock)


def test_add_and_query_product_integration(uow_factory_integration):
    # Add product
    prod = create_product(uow_factory_integration, nombre="Ibuprofeno", codigo="IBU400", precio="123,45", detalle="Caja x10", cod_barras="779...", stock="7")

    assert prod.id_producto is not None

    # Query by id
    qp = QueryProducts(uow_factory_integration)
    fetched = qp.get_by_id(prod.id_producto)

    assert fetched is not None
    assert fetched.nombre == "Ibuprofeno"
    assert fetched.codigo == "IBU400"
    assert fetched.precio.value == Decimal("123.45")
    assert fetched.stock.value == 7


def test_edit_product_info_integration(uow_factory_integration):
    prod = create_product(uow_factory_integration, nombre="Paracetamol", codigo="PARA500", precio="200,00", detalle="Caja x16", cod_barras="123", stock="3")

    epi = EditProductInfo(uow_factory_integration)
    epi.execute(
        id_producto=prod.id_producto,
        nombre="Paracetamol Forte",
        codigo="PARA650",
        precio="250,50",
        stock_param="10",
        detalle="Caja x 20",
        codigo_de_barras="456",
    )

    qp = QueryProducts(uow_factory_integration)
    updated = qp.get_by_id(prod.id_producto)

    assert updated is not None
    assert updated.nombre == "Paracetamol Forte"
    assert updated.codigo == "PARA650"
    assert updated.precio.value == Decimal("250.50")
    assert updated.stock.value == 10


def test_edit_stock_integration(uow_factory_integration):
    prod = create_product(uow_factory_integration, stock="0")

    es = EditStock(uow_factory_integration)
    es.set_stock(prod.id_producto, 5)

    qp = QueryProducts(uow_factory_integration)
    mid = qp.get_by_id(prod.id_producto)
    assert mid is not None and mid.stock.value == 5

    es.add_stock(prod.id_producto, 3)
    end = qp.get_by_id(prod.id_producto)
    assert end is not None and end.stock.value == 8


def test_update_price_integration(uow_factory_integration):
    p1 = create_product(uow_factory_integration, nombre="A", precio="100,00")
    p2 = create_product(uow_factory_integration, nombre="B", precio="50,00")

    up = UpdatePrice(uow_factory_integration)
    up.update_selected([p1.id_producto, p2.id_producto], percent=10)  # +10%

    qp = QueryProducts(uow_factory_integration)
    a = qp.get_by_id(p1.id_producto)
    b = qp.get_by_id(p2.id_producto)

    assert a is not None and a.precio.value == Decimal("110.00")
    assert b is not None and b.precio.value == Decimal("55.00")


def test_register_sale_and_query_sales_integration(uow_factory_integration):
    prod = create_product(uow_factory_integration, nombre="Jarabe", precio="33,33", stock="10")

    rs = RegisterSale(uow_factory_integration)
    sale_date = datetime.now().replace(microsecond=0)
    sale_id = rs.execute(prod.id_producto, amount=2, date=sale_date)

    assert isinstance(sale_id, int) and sale_id > 0

    # Product stock decreased
    qp = QueryProducts(uow_factory_integration)
    after = qp.get_by_id(prod.id_producto)
    assert after is not None and after.stock.value == 8

    # Query sales by day and range
    qs = QuerySales(uow_factory_integration)
    same_day_sales = qs.by_date(sale_date)
    assert len(same_day_sales) == 1
    assert same_day_sales[0].id_venta == sale_id
    # total price = 2 * 33.33 = 66.66 (with ROUND_HALF_UP it stays 66.66)
    assert same_day_sales[0].total_price.value == Decimal("66.66")

    next_day = sale_date + timedelta(days=1)
    range_sales = qs.by_range(sale_date - timedelta(hours=1), next_day)
    assert any(s.id_venta == sale_id for s in range_sales)
