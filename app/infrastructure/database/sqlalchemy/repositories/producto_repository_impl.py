from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import Select, func, or_, select, update
from sqlalchemy.orm import Session

from app.application.ports.producto_repository import IProductoRepository, ProductFilter
from app.domain.models.precio import Precio
from app.domain.models.producto import Producto
from app.domain.models.stock import Stock
from app.infrastructure.database.sqlalchemy.mappers.producto_mapper import ProductoMapper
from app.infrastructure.database.sqlalchemy.models.producto_orm import ProductoORM


class ProductoRepositoryImpl(IProductoRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_product(self, product: Producto) -> None:
        product_orm = ProductoMapper.new_to_orm_producto(product)
        self.session.add(product_orm)
        self.session.flush()
        product.id_producto = product_orm.id

    def _apply_filters(self, stmt: Select, filtro: ProductFilter) -> Select:
        if hasattr(ProductoORM, "activo") and not filtro.include_inactive:
            stmt = stmt.where(ProductoORM.activo.is_(True))

        if filtro.only_no_stock:
            stmt = stmt.where(ProductoORM.stock < 1)

        if filtro.search is not None:
            term = filtro.search.strip()
            if term:
                pattern = f"%{term}%"
                stmt = stmt.where(
                    or_(
                        ProductoORM.nombre.ilike(pattern),
                        ProductoORM.detalle.ilike(pattern),
                        ProductoORM.codigo.ilike(pattern),
                        ProductoORM.codigo_de_barras.ilike(pattern),
                    )
                )
        return stmt

    def list_products(self, filtro: ProductFilter | None = None) -> list[Producto]:
        active_filter = filtro or ProductFilter()
        stmt = self._apply_filters(select(ProductoORM), active_filter)

        if active_filter.alphabetical:
            stmt = stmt.order_by(ProductoORM.nombre.asc(), ProductoORM.id.asc())
        else:
            stmt = stmt.order_by(ProductoORM.id.asc())

        if active_filter.offset > 0:
            stmt = stmt.offset(active_filter.offset)
        if active_filter.limit is not None:
            stmt = stmt.limit(active_filter.limit)

        rows = self.session.scalars(stmt).all()
        return [ProductoMapper.to_domain_producto(prod) for prod in rows]

    def count_products(self, filtro: ProductFilter | None = None) -> int:
        active_filter = filtro or ProductFilter()
        stmt = self._apply_filters(select(func.count(ProductoORM.id)), active_filter)
        return int(self.session.scalar(stmt) or 0)

    def get_by_id(self, product_id: int) -> Producto | None:
        found = self.session.get(ProductoORM, product_id)
        if found is None:
            return None
        return ProductoMapper.to_domain_producto(found)

    def get_by_barcode(self, barcode: str) -> Producto | None:
        cleaned = (barcode or "").strip()
        if not cleaned:
            return None
        stmt = select(ProductoORM).where(ProductoORM.codigo_de_barras == cleaned)
        if hasattr(ProductoORM, "activo"):
            stmt = stmt.where(ProductoORM.activo.is_(True))
        found = self.session.scalars(stmt).first()
        if found is None:
            return None
        return ProductoMapper.to_domain_producto(found)

    def get_products_by_id_list(self, ids_buscadas: list[int]) -> list[Producto]:
        if not ids_buscadas:
            return []
        stmt = select(ProductoORM).where(ProductoORM.id.in_(ids_buscadas))
        rows = self.session.scalars(stmt).all()
        return [ProductoMapper.to_domain_producto(prod) for prod in rows]

    def add_stock(self, id_producto: int, cantidad: int) -> None:
        stmt = (
            update(ProductoORM)
            .where(ProductoORM.id == id_producto)
            .values(stock=ProductoORM.stock + cantidad)
        )
        self.session.execute(stmt)

    def add_stock_to_multiple_products(self, ids_list: list[int], stock_to_add: int) -> None:
        if not ids_list:
            return
        stmt = (
            update(ProductoORM)
            .where(ProductoORM.id.in_(ids_list))
            .values(stock=ProductoORM.stock + stock_to_add)
        )
        self.session.execute(stmt)

    def set_stock(self, id_producto: int, stock: Stock) -> None:
        stmt = (
            update(ProductoORM)
            .where(ProductoORM.id == id_producto)
            .values(stock=stock.value)
        )
        self.session.execute(stmt)

    def set_stock_bulk(self, ids_list: list[int], new_stock: Stock) -> None:
        if not ids_list:
            return
        stmt = (
            update(ProductoORM)
            .where(ProductoORM.id.in_(ids_list))
            .values(stock=new_stock.value)
        )
        self.session.execute(stmt)

    def update_all_prices(self, percent_multiplier: Decimal = Decimal("1")) -> None:
        mult = Decimal(str(percent_multiplier))
        stmt = select(ProductoORM)
        if hasattr(ProductoORM, "activo"):
            stmt = stmt.where(ProductoORM.activo.is_(True))
        productos = self.session.scalars(stmt).all()
        for producto in productos:
            new_price = (Decimal(producto.precio) * mult).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            producto.precio = new_price

    def update_selected_product_prices(
        self, ids_list: list[int], percent_multiplier: Decimal = Decimal("1")
    ) -> None:
        if not ids_list:
            return
        mult = Decimal(str(percent_multiplier))
        stmt = select(ProductoORM).where(ProductoORM.id.in_(ids_list))
        productos = self.session.scalars(stmt).all()
        for producto in productos:
            new_price = (Decimal(producto.precio) * mult).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            producto.precio = new_price

    def update_price_to_new_value(self, ids_list: list[int], new_price: Precio) -> None:
        if not ids_list:
            return
        stmt = (
            update(ProductoORM)
            .where(ProductoORM.id.in_(ids_list))
            .values(precio=new_price.value)
        )
        self.session.execute(stmt)

    def update_info_product(self, producto_new: Producto) -> None:
        producto_old = self.session.get(ProductoORM, producto_new.id_producto)
        if producto_old:
            producto_old.nombre = producto_new.nombre
            producto_old.detalle = producto_new.detalle
            producto_old.codigo = producto_new.codigo
            producto_old.codigo_de_barras = producto_new.codigo_de_barras
            producto_old.precio = producto_new.precio.value
            producto_old.stock = producto_new.stock.value
            if hasattr(producto_old, "activo"):
                producto_old.activo = producto_new.activo

    def set_active(self, product_id: int, active: bool) -> bool:
        producto = self.session.get(ProductoORM, product_id)
        if producto is None:
            return False
        if hasattr(producto, "activo"):
            producto.activo = active
        return True
