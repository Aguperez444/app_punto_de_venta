from datetime import datetime
from decimal import Decimal
import pytest

from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.precio import Precio
from app.domain.models.producto import Producto
from app.domain.models.stock import Stock
from app.domain.models.venta import Venta
from app.infrastructure.export.csv_exporter import CsvExporter


@pytest.mark.unit
def test_csv_exporter_exports_sales_with_multiple_items(tmp_path):
    p1 = Producto(1, "Ibuprofeno 400", "IBU400", Precio(Decimal("120.50")), "Caja", "7791", Stock(0))
    p2 = Producto(2, "Jarabe Niños", "JAR01", Precio(Decimal("350.00")), "", "7792", Stock(-2))

    venta = Venta.nueva(datetime(2026, 8, 21, 14, 15, 0))
    venta.id_venta = 7
    venta.agregar_detalle(DetalleVenta(1, 1, 7, 2, p1.precio, product=p1))
    venta.agregar_detalle(DetalleVenta(2, 2, 7, 1, p2.precio, product=p2))

    out = CsvExporter.export_sales([venta], tmp_path / "ventas.csv")
    content = out.read_text(encoding="utf-8-sig")

    assert "ID Venta;Fecha;Hora;Producto" in content
    assert "Ibuprofeno 400;IBU400;2;120.50;241.00;591.00" in content
    assert "Jarabe Niños;JAR01;1;350.00;350.00;591.00" in content


@pytest.mark.unit
def test_csv_exporter_exports_products_including_negative_stock(tmp_path):
    products = [
        Producto(1, "Amoxicilina", "AMO500", Precio(Decimal("890.00")), "Blister", "7799", Stock(-3)),
        Producto(2, "Alcohol 70%", "ALC70", Precio(Decimal("450.25")), "500ml", "", Stock(0)),
    ]

    out = CsvExporter.export_products(products, tmp_path / "faltantes.csv")
    content = out.read_text(encoding="utf-8-sig")

    assert "ID;Nombre;Código;Precio;Detalle;Código de barras;Stock" in content
    assert "Amoxicilina;AMO500;890.00;Blister;7799;-3" in content
    assert "Alcohol 70%;ALC70;450.25;500ml;;0" in content
