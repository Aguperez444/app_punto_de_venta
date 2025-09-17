from Database.db_session import SessionLocal
from Models.producto import Producto

class ProductoRepository:


    @staticmethod
    def save_product(product: Producto) -> None:
        with SessionLocal() as session:
            try:
                session.add(product)
                session.commit()
                session.refresh(product)
            except Exception:
                session.rollback()
                raise


    @staticmethod
    def get_all_products() -> list[Producto]:
        with SessionLocal() as session:
            return session.query(Producto).all()


    @staticmethod
    def get_all_products_alphabetically() -> list[Producto]:
        with SessionLocal() as session:
            return session.query(Producto).order_by(Producto.producto).all()


    @staticmethod
    def get_filtered(buscado: str) -> list[Producto] | None:
        if buscado == '':
            return None

        with SessionLocal() as session:
            encontrado = session.query(Producto).filter(
                (Producto.producto.ilike(f'%{buscado}%')) |
                (Producto.detalle.ilike(f'%{buscado}%')) |
                (Producto.codigo.ilike(f'%{buscado}%')) |
                (Producto.codigo_de_barras.ilike(f'%{buscado}%'))
            ).all()

        return encontrado

    @staticmethod
    def get_filtered_alphabetically(search_criteria: str) -> list[Producto] | None:
        if search_criteria == '':
            return None

        with SessionLocal() as session:
            encontrado = session.query(Producto).filter(
                (Producto.producto.ilike(f'%{search_criteria}%')) |
                (Producto.detalle.ilike(f'%{search_criteria}%')) |
                (Producto.codigo.ilike(f'%{search_criteria}%')) |
                (Producto.codigo_de_barras.ilike(f'%{search_criteria}%'))
            ).order_by(Producto.producto).all()

        return encontrado


    @staticmethod
    def get_all_no_stock() -> list[Producto] | None:
        with SessionLocal() as session:
            return session.query(Producto).filter(Producto.stock < 1).all()


    @staticmethod
    def get_filtered_no_stock(buscado: str) -> list[Producto] | None:
        if buscado == '':
            return None

        with SessionLocal() as session:
            encontrado = session.query(Producto).filter(
                ((Producto.producto.ilike(f'%{buscado}%')) |
                 (Producto.detalle.ilike(f'%{buscado}%')) |
                 (Producto.codigo.ilike(f'%{buscado}%')) |
                 (Producto.codigo_de_barras.ilike(f'%{buscado}%'))) &
                (Producto.stock < 1)
            ).all()

        return encontrado


    @staticmethod
    def get_filtered_no_stock_alphabetically(buscado: str) -> list[Producto] | None:
        if buscado == '':
            return None

        with SessionLocal() as session:
            encontrado = session.query(Producto).filter(
                ((Producto.producto.ilike(f'%{buscado}%')) |
                 (Producto.detalle.ilike(f'%{buscado}%')) |
                 (Producto.codigo.ilike(f'%{buscado}%')) |
                 (Producto.codigo_de_barras.ilike(f'%{buscado}%'))) &
                (Producto.stock < 1)
            ).order_by(Producto.producto).all()

        return encontrado


    @staticmethod
    def get_product_by_id(product_id: int) -> Producto | None:
        with SessionLocal() as session:
            return session.get(Producto, product_id)


    @staticmethod
    def get_products_by_id_list(ids_buscadas: list[int]) -> list[Producto] | None:
        if not ids_buscadas:
            return None

        with SessionLocal() as session:
            encontrado = session.query(Producto).filter(Producto.id.in_(ids_buscadas)).all()

        return encontrado


    @staticmethod
    def add_stock(id_producto: int, cantidad: int) -> None:
        with SessionLocal() as session:
            producto = session.query(Producto).filter_by(id=id_producto).first()
            if producto:
                producto.stock += cantidad
                session.commit()


    @staticmethod
    def add_stock_to_multiple_products(ids_list: list, stock_to_add: int) -> None:

        with SessionLocal() as session:
            productos = session.query(Producto).filter(Producto.id.in_(ids_list)).all()
            for producto in productos:
                producto.stock += stock_to_add
            session.commit()



    @staticmethod
    def update_stock(id_producto: int, cantidad: int) -> None:
        with SessionLocal() as session:
            producto = session.query(Producto).filter_by(id=id_producto).first()
            if producto:
                producto.stock = cantidad
                session.commit()


    @staticmethod
    def update_all_prices(percent_multiplier: float=1) -> None:

        with SessionLocal() as session:
            productos = session.query(Producto).all()

            for producto in productos:

                new_price = round((float(producto.precio) * percent_multiplier), 2) # Calculate new price
                producto.precio = new_price

            session.commit()


    @staticmethod
    def update_selected_product_prices(ids_list: list, percent_multiplier: float=1) -> None:

        with SessionLocal() as session:
            productos = session.query(Producto).filter(Producto.id.in_(ids_list)).all()

            for producto in productos:
                new_price = round((producto.precio * percent_multiplier), 2) # Calculate new price
                producto.precio = new_price

            session.commit()


    @staticmethod
    def update_price_to_new_value(ids_list: list, new_price: float) -> None:

        with SessionLocal() as session:
            productos = session.query(Producto).filter(Producto.id.in_(ids_list)).all()
            for producto in productos:
                producto.precio = new_price
            session.commit()


    @staticmethod
    def update_stock_to_multiple_products(ids_list: list, new_stock: int) -> None:

        with SessionLocal() as session:
            productos = session.query(Producto).filter(Producto.id.in_(ids_list)).all()
            for producto in productos:
                producto.stock += new_stock
            session.commit()


    @staticmethod
    def update_info_product_bdd(producto_new: Producto) -> None:
        with SessionLocal() as session:
            producto_old = session.get(Producto, producto_new.id)
            if producto_old:
                producto_old.producto = producto_new.producto
                producto_old.detalle = producto_new.detalle
                producto_old.codigo = producto_new.codigo
                producto_old.codigo_de_barras = producto_new.codigo_de_barras
                producto_old.precio = producto_new.precio
                producto_old.stock = producto_new.stock

                session.commit()



