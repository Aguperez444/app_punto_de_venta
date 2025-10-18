from decimal import Decimal
from freezegun import freeze_time
from app.domain.models.venta import Venta
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.precio import Precio


def test_venta_nueva_has_zero_total_and_now_date():
    with freeze_time("2025-01-01 10:00:00"):
        v = Venta.nueva()
        assert v.total == Decimal("0.00")
        assert v.fecha.year == 2025
        assert v.fecha.month == 1
        assert v.fecha.day == 1


def test_venta_aggregate_and_update_price():
    v = Venta.nueva()
    v.agregar_detalle(DetalleVenta.create_new(1, 2, Precio(Decimal("10.00"))))
    v.agregar_detalle(DetalleVenta.create_new(2, 1, Precio(Decimal("5.505"))))
    # total = 2*10 + 1*5.505=25.505 -> quantize HALF_UP to 25.51 in Venta.total
    assert v.total == Decimal("25.51")
    v.update_price()
    assert str(v.total_price) == "$25,51"
