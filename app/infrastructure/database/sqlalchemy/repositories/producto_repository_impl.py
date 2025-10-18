from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.application.ports.producto_repository import IProductoRepository
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock
from app.infrastructure.database.sqlalchemy.orm import ProductoORM, ProductoMapper
from app.domain.models.producto import Producto

class ProductoRepositoryImpl(IProductoRepository):

    def __init__(self, session: Session):
        self.session = session


    def save_product(self, product: Producto) -> None:
            product_orm = ProductoMapper.new_to_orm_producto(product)
            self.session.add(product_orm)
            self.session.flush()
            product.id_producto = product_orm.id



    def get_all_products(self) -> list[Producto]:
        found = self.session.query(ProductoORM).all()
        # el typechecker detecta mal lo que devuelve el query().all()
        # noinspection PyTypeChecker
        return [ProductoMapper.to_domain_producto(prod) for prod in found]


    def get_all_products_alphabetically(self) -> list[Producto]:
        found = self.session.query(ProductoORM).order_by(ProductoORM.nombre).all()
        # el typechecker detecta mal lo que devuelve el query().all()
        # noinspection PyTypeChecker
        return [ProductoMapper.to_domain_producto(prod) for prod in found]



    def get_filtered(self, buscado: str) -> list[Producto] | None:
        if buscado == '':
            return None


        found = self.session.query(ProductoORM).filter(
            (ProductoORM.nombre.ilike(f'%{buscado}%')) |
            (ProductoORM.detalle.ilike(f'%{buscado}%')) |
            (ProductoORM.codigo.ilike(f'%{buscado}%')) |
            (ProductoORM.codigo_de_barras.ilike(f'%{buscado}%'))
        ).all()

        if found:
            # el typechecker detecta mal lo que devuelve el filter().all()
            # noinspection PyTypeChecker
            return [ProductoMapper.to_domain_producto(prod) for prod in found]

        return None


    def get_filtered_alphabetically(self, search_criteria: str) -> list[Producto] | None:
        if search_criteria == '':
            return None


        found = self.session.query(ProductoORM).filter(
            (ProductoORM.nombre.ilike(f'%{search_criteria}%')) |
            (ProductoORM.detalle.ilike(f'%{search_criteria}%')) |
            (ProductoORM.codigo.ilike(f'%{search_criteria}%')) |
            (ProductoORM.codigo_de_barras.ilike(f'%{search_criteria}%'))
        ).order_by(ProductoORM.nombre).all()

        if found:
            # el typechecker detecta mal lo que devuelve el filter().all()
            # noinspection PyTypeChecker
            return [ProductoMapper.to_domain_producto(prod) for prod in found]

        return None


    def get_all_no_stock(self) -> list[Producto] | None:
        found = self.session.query(ProductoORM).filter(ProductoORM.stock < 1).all()

        if found:
            # el typechecker detecta mal lo que devuelve el filter().all()
            # noinspection PyTypeChecker
            return [ProductoMapper.to_domain_producto(prod) for prod in found]
        return None


    def get_all_no_stock_alphabetically(self) -> list[Producto] | None:
        found = self.session.query(ProductoORM).filter(ProductoORM.stock < 1).order_by(ProductoORM.nombre).all()

        if found:
            # el typechecker detecta mal lo que devuelve el filter().all()
            # noinspection PyTypeChecker
            return [ProductoMapper.to_domain_producto(prod) for prod in found]
        return None


    def get_filtered_no_stock(self, search_criteria: str) -> list[Producto] | None:
        if search_criteria == '':
            return None


        found = self.session.query(ProductoORM).filter(
            ((ProductoORM.nombre.ilike(f'%{search_criteria}%')) |
             (ProductoORM.detalle.ilike(f'%{search_criteria}%')) |
             (ProductoORM.codigo.ilike(f'%{search_criteria}%')) |
             (ProductoORM.codigo_de_barras.ilike(f'%{search_criteria}%'))) &
            (ProductoORM.stock < 1)
        ).all()


        if found:
            # el typechecker detecta mal lo que devuelve el query().all()
            # noinspection PyTypeChecker
            return [ProductoMapper.to_domain_producto(prod) for prod in found]
        return None


    def get_filtered_no_stock_alphabetically(self, search_criteria: str) -> list[Producto] | None:
        if search_criteria == '':
            return None


        found = self.session.query(ProductoORM).filter(
            ((ProductoORM.nombre.ilike(f'%{search_criteria}%')) |
             (ProductoORM.detalle.ilike(f'%{search_criteria}%')) |
             (ProductoORM.codigo.ilike(f'%{search_criteria}%')) |
             (ProductoORM.codigo_de_barras.ilike(f'%{search_criteria}%'))) &
            (ProductoORM.stock < 1)
        ).order_by(ProductoORM.nombre).all()

        if found:
            # el typechecker detecta mal lo que devuelve el query().all()
            # noinspection PyTypeChecker
            return [ProductoMapper.to_domain_producto(prod) for prod in found]
        return None


    def get_by_id(self, product_id: int) -> Producto | None:

        found = self.session.get(ProductoORM, product_id)

        if found:
            # el typechecker detecta mal lo que devuelve el get()
            # noinspection PyTypeChecker
            return ProductoMapper.to_domain_producto(found)
        return None



    def get_products_by_id_list(self, ids_buscadas: list[int]) -> list[Producto] | None:
        if not ids_buscadas:
            return None


        found = self.session.query(ProductoORM).filter(ProductoORM.id.in_(ids_buscadas)).all()

        if found:
            # el typechecker detecta mal lo que devuelve el query().all()
            # noinspection PyTypeChecker
            return [ProductoMapper.to_domain_producto(prod) for prod in found]
        return None


    def add_stock(self, id_producto: int, cantidad: int) -> None:

        producto = self.session.query(ProductoORM).filter_by(id=id_producto).first()
        if producto:
            producto.stock += cantidad
        # el commit se hace en el uow


    def add_stock_to_multiple_products(self, ids_list: list, stock_to_add: int) -> None:

        productos = self.session.query(ProductoORM).filter(ProductoORM.id.in_(ids_list)).all()
        for producto in productos:
            producto.stock += stock_to_add
        # el commit se hace en el uow



    def set_stock(self, id_producto: int, stock: Stock) -> None:
        producto = self.session.query(ProductoORM).filter_by(id=id_producto).first()
        if producto:
            producto.stock = stock.value
            # el commit se hace en el uow



    def update_all_prices(self, percent_multiplier: float=1) -> None:
        productos = self.session.query(ProductoORM).all()

        for producto in productos:
            # el typechecker detecta mal lo que devuelve el query().all()
            # noinspection PyTypeChecker
            new_price = Decimal((Decimal(producto.precio) * Decimal(percent_multiplier))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) # Calculate new price
            producto.precio = new_price

        # el commit se hace en el uow


    def update_selected_product_prices(self, ids_list: list, percent_multiplier: float=1) -> None:
        productos = self.session.query(ProductoORM).filter(ProductoORM.id.in_(ids_list)).all()

        for producto in productos:
            # el typechecker detecta mal lo que devuelve el query().all()
            # noinspection PyTypeChecker
            new_price = Decimal((Decimal(producto.precio) * Decimal(percent_multiplier))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) # Calculate new price
            producto.precio = new_price

        # el commit se hace en el uow


    def update_price_to_new_value(self, ids_list: list, new_price: Precio) -> None:
        productos = self.session.query(ProductoORM).filter(ProductoORM.id.in_(ids_list)).all()
        for producto in productos:
            producto.precio = new_price.value
        # el commit se hace en el uow


    def set_stock_bulk(self, ids_list: list, new_stock: Stock) -> None:
        productos = self.session.query(ProductoORM).filter(ProductoORM.id.in_(ids_list)).all()
        for producto in productos:
            producto.stock += new_stock.value
        # el commit se hace en el uow


    def update_info_product(self, producto_new: Producto) -> None:
        producto_old = self.session.get(ProductoORM, producto_new.id_producto)
        if producto_old:
            producto_old.nombre = producto_new.nombre
            producto_old.detalle = producto_new.detalle
            producto_old.codigo = producto_new.codigo
            producto_old.codigo_de_barras = producto_new.codigo_de_barras
            producto_old.precio = producto_new.precio.value
            producto_old.stock = producto_new.stock.value

            # el commit se hace en el uow



