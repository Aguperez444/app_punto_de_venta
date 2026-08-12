from datetime import datetime
from decimal import Decimal
import pytest

from app.application.dto.product_dto import ProductDTO
from app.application.dto.sales_dto import SaleDetailDTO, SaleSummaryDTO
from app.application.use_cases.delete_product import DeleteProduct, RestoreProduct
from app.domain.custom_errors import NotFoundProductError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.precio import Precio
from app.domain.models.producto import Producto
from app.domain.models.stock import Stock
from app.domain.models.venta import Venta


class _FakeProductRepo:
    def __init__(self, existing_ids: set[int]):
        self.active_map = {pid: True for pid in existing_ids}

    def set_active(self, product_id: int, active: bool) -> bool:
        if product_id not in self.active_map:
            return False
        self.active_map[product_id] = active
        return True


class _FakeUoW:
    def __init__(self, repo):
        self.product_repo = repo
        self.sale_repo = None
        self.commits = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def commit(self):
        self.commits += 1

    def rollback(self):
        pass


@pytest.mark.unit
def test_delete_and_restore_product_success():
    repo = _FakeProductRepo({10})
    uow = _FakeUoW(repo)

    DeleteProduct(lambda: uow).execute(10)
    assert repo.active_map[10] is False
    assert uow.commits == 1

    RestoreProduct(lambda: uow).execute(10)
    assert repo.active_map[10] is True
    assert uow.commits == 2


@pytest.mark.unit
def test_delete_and_restore_missing_product_raises():
    repo = _FakeProductRepo(set())
    uow = _FakeUoW(repo)

    with pytest.raises(NotFoundProductError):
        DeleteProduct(lambda: uow).execute(999)
    with pytest.raises(NotFoundProductError):
        RestoreProduct(lambda: uow).execute(999)
    assert uow.commits == 0


@pytest.mark.unit
def test_dtos_build_from_domain_objects():
    p1 = Producto(1, "Ibuprofeno", "IBU", Precio(Decimal("100.00")), "Caja", "7791", Stock(5))
    p2 = Producto(2, "Paracetamol", "PAR", Precio(Decimal("50.50")), "", "", Stock(-1))
    pdto = ProductDTO.from_domain(p1)
    assert pdto.precio_str == "$100,00"
    assert pdto.activo is True

    venta = Venta.nueva(datetime(2026, 8, 12, 10, 30, 0))
    venta.id_venta = 42
    d1 = DetalleVenta(1, 1, 42, 2, p1.precio, product=p1)
    d2 = DetalleVenta(2, 2, 42, 1, p2.precio, product=p2)
    venta.agregar_detalle(d1)
    venta.agregar_detalle(d2)

    summary = SaleSummaryDTO.from_domain(venta)
    assert summary.venta_id == 42
    assert summary.resumen_productos == "Ibuprofeno (+1 más)"
    assert summary.cantidad_total == 3
    assert summary.total_str == "$250,50"

    detail = SaleDetailDTO.from_domain(venta)
    assert len(detail.items) == 2
    assert detail.items[0].subtotal_str == "$200,00"
    assert detail.items[1].subtotal_str == "$50,50"
