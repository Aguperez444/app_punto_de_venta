from datetime import datetime, timedelta
from decimal import Decimal
import pytest

from app.application.ports.producto_repository import ProductFilter
from app.application.use_cases.add_product import AddProduct
from app.application.use_cases.delete_product import DeleteProduct, RestoreProduct
from app.application.use_cases.edit_product_info import EditProductInfo
from app.application.use_cases.edit_stock import EditStock
from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.query_sales import QuerySales
from app.application.use_cases.register_sale import RegisterSale, SaleItemInput
from app.application.use_cases.update_price import UpdatePrice
from app.infrastructure.ui.tkinter.views.windows.find_bdd_window import run_alembic_upgrade

pytestmark = pytest.mark.integration


def create_product(
    uow_factory,
    nombre="Prod A",
    codigo="PA",
    precio="100,00",
    detalle="",
    cod_barras="",
    stock="5",
):
    add_uc = AddProduct(uow_factory)
    return add_uc.execute(nombre, codigo, precio, detalle, cod_barras, stock)


def test_add_and_query_product_integration(uow_factory_integration):
    prod = create_product(
        uow_factory_integration,
        nombre="Ibuprofeno",
        codigo="IBU400",
        precio="123,45",
        detalle="Caja x10",
        cod_barras="7790001112223",
        stock="7",
    )

    assert prod.id_producto is not None

    qp = QueryProducts(uow_factory_integration)
    fetched = qp.get_by_id(prod.id_producto)
    assert fetched is not None
    assert fetched.nombre == "Ibuprofeno"
    assert fetched.codigo == "IBU400"
    assert fetched.precio.value == Decimal("123.45")
    assert fetched.stock.value == 7

    by_barcode = qp.get_by_barcode("7790001112223")
    assert by_barcode is not None and by_barcode.id_producto == prod.id_producto

    assert qp.get_filtered("NO_EXISTE_XYZ") == []


def test_edit_product_info_integration(uow_factory_integration):
    prod = create_product(
        uow_factory_integration,
        nombre="Paracetamol",
        codigo="PARA500",
        precio="200,00",
        detalle="Caja x16",
        cod_barras="123",
        stock="3",
    )

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


def test_edit_stock_bulk_and_negative_integration(uow_factory_integration):
    p1 = create_product(uow_factory_integration, nombre="P1", codigo="C1", stock="5")
    p2 = create_product(uow_factory_integration, nombre="P2", codigo="C2", stock="2")

    es = EditStock(uow_factory_integration)
    # set_stock_bulk fija el valor (no suma)
    es.set_stock_bulk([p1.id_producto, p2.id_producto], 10)

    qp = QueryProducts(uow_factory_integration)
    assert qp.get_by_id(p1.id_producto).stock.value == 10
    assert qp.get_by_id(p2.id_producto).stock.value == 10

    # Restar más que el stock actual queda negativo (permitido por regla de negocio)
    es.add_stock_to_multiple_products([p1.id_producto, p2.id_producto], -14)
    assert qp.get_by_id(p1.id_producto).stock.value == -4
    assert qp.get_by_id(p2.id_producto).stock.value == -4

    no_stock = qp.get_no_stock()
    assert len(no_stock) == 2


def test_update_price_all_selected_and_manual_integration(uow_factory_integration):
    p1 = create_product(uow_factory_integration, nombre="A", codigo="A", precio="100,00")
    p2 = create_product(uow_factory_integration, nombre="B", codigo="B", precio="50,00")

    up = UpdatePrice(uow_factory_integration)
    up.update_selected([p1.id_producto, p2.id_producto], percent="10")

    qp = QueryProducts(uow_factory_integration)
    assert qp.get_by_id(p1.id_producto).precio.value == Decimal("110.00")
    assert qp.get_by_id(p2.id_producto).precio.value == Decimal("55.00")

    up.update_all("12,5")
    assert qp.get_by_id(p1.id_producto).precio.value == Decimal("123.75")
    assert qp.get_by_id(p2.id_producto).precio.value == Decimal("61.88")

    up.update_to_new_value([p2.id_producto], "$99,90")
    assert qp.get_by_id(p2.id_producto).precio.value == Decimal("99.90")


def test_register_sale_cart_negative_stock_and_soft_delete_integration(uow_factory_integration):
    p1 = create_product(uow_factory_integration, nombre="Jarabe", codigo="JAR", precio="33,33", stock="1")
    p2 = create_product(uow_factory_integration, nombre="Alcohol", codigo="ALC", precio="50,00", stock="0")

    rs = RegisterSale(uow_factory_integration)
    sale_date = datetime(2026, 8, 22, 11, 30, 0)
    sale_id = rs.execute_cart(
        [
            SaleItemInput(p1.id_producto, 2),
            SaleItemInput(p2.id_producto, 3),
        ],
        date=sale_date,
    )

    assert isinstance(sale_id, int) and sale_id > 0

    qp = QueryProducts(uow_factory_integration)
    assert qp.get_by_id(p1.id_producto).stock.value == -1
    assert qp.get_by_id(p2.id_producto).stock.value == -3

    # Soft-delete de un producto vendido preserva integridad de ventas previas
    DeleteProduct(uow_factory_integration).execute(p1.id_producto)
    assert len(qp.get_all()) == 1
    assert len(qp.get_all(include_inactive=True)) == 2
    assert qp.count_products(ProductFilter(include_inactive=False)) == 1

    qs = QuerySales(uow_factory_integration)
    fetched_sale = qs.get_by_id(sale_id)
    assert fetched_sale is not None
    assert len(fetched_sale.detalles) == 2
    assert fetched_sale.total_price.value == Decimal("216.66")

    same_day = qs.by_date(sale_date)
    assert len(same_day) == 1
    next_day = sale_date + timedelta(days=1)
    assert any(s.id_venta == sale_id for s in qs.by_range(sale_date - timedelta(hours=1), next_day))

    # Reactivar producto
    RestoreProduct(uow_factory_integration).execute(p1.id_producto)
    assert len(qp.get_all()) == 2


def test_alembic_upgrade_helper_creates_schema(tmp_path):
    db_file = tmp_path / "alembic_int.db"
    ok, msg = run_alembic_upgrade(f"sqlite:///{db_file}")
    assert ok is True, msg


def test_alembic_upgrade_migrates_legacy_db_without_activo_column(tmp_path):
    import sqlite3
    from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import build_uow_factory

    db_file = tmp_path / "legacy_farma.db"
    conn = sqlite3.connect(db_file)
    try:
        conn.execute(
            """
            CREATE TABLE "Productos" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(150) NOT NULL,
                codigo VARCHAR(50) NOT NULL,
                precio NUMERIC NOT NULL,
                detalle VARCHAR(255),
                codigo_de_barras VARCHAR(100),
                stock INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            INSERT INTO "Productos" (nombre, codigo, precio, detalle, codigo_de_barras, stock)
            VALUES ('Elixir Legacy', 'ELX1', 150.00, 'Frasco', '779001', 4)
            """
        )
        conn.commit()
    finally:
        conn.close()

    db_url = f"sqlite:///{db_file}"
    ok, msg = run_alembic_upgrade(db_url)
    assert ok is True, msg

    factory, engine = build_uow_factory(db_url)
    try:
        qp = QueryProducts(factory)
        found = qp.get_filtered("el")
        assert len(found) == 1
        assert found[0].nombre == "Elixir Legacy"
        assert found[0].activo is True
    finally:
        engine.dispose()


def test_query_products_tolerates_legacy_rows_with_blank_nombre_or_codigo(session_factory, uow_factory_integration):
    from app.infrastructure.database.sqlalchemy.models.producto_orm import ProductoORM

    with session_factory() as session:
        session.add(
            ProductoORM(
                nombre="",
                codigo="",
                precio=Decimal("10.00"),
                detalle=None,
                codigo_de_barras=None,
                stock=0,
                activo=True,
            )
        )
        session.commit()

    qp = QueryProducts(uow_factory_integration)
    all_products = qp.get_all()
    assert len(all_products) == 1
    assert all_products[0].nombre == ""
    assert all_products[0].codigo == ""
