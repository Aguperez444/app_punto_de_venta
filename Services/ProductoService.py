from Models.Producto import Producto
from Persistence.repositorys.producto_repository import ProductoRepository
from custom_errors import DomainValidationError


class ProductoService:
    def __init__(self):
        self.repo = ProductoRepository()


    @staticmethod
    def validate_price(precio: str) -> bool:
        return precio.isdigit() or (precio.startswith('$') and precio[1:].isdigit())

    @staticmethod
    def validate_stock(stock: str) -> bool:
        return stock.isdigit() and int(stock) >= 0

    @staticmethod
    def transform_price_to_str(precio: float) -> str:
        return f"${precio}"

    @staticmethod
    def transform_price_to_float(precio: str) -> float:
        price_str = precio.replace(',', '.').replace('$', '') # Normalize price string to convert to float
        price_float = round(float(price_str), 2) # Convert to float and round to 2 decimal places
        return price_float

    @staticmethod
    def create_new_product(producto: str, codigo: str,
                           precio: str, detalle: str, codigo_de_barras: str, stock: str) -> Producto:
        # Validaciones
        if not ProductoService.validate_price(precio):
            raise DomainValidationError("El precio del producto solo puede contener números enteros y el símbolo $")
        if not ProductoService.validate_stock(stock):
            raise DomainValidationError("El campo stock solo debe contener números enteros positivos.")

        # crear objeto producto
        nuevo_producto = Producto(
            producto=producto,
            codigo=codigo,
            precio=int(precio.replace("$", "")),
            detalle=detalle,
            codigo_de_barras=codigo_de_barras,
            stock=int(stock)
        )

        #retornar el producto creado
        return nuevo_producto


    def get_all_products(self) -> list:
        return self.repo.get_all_products()

    def get_all_products_no_stock(self) -> list:
        return self.repo.get_all_no_stock()

    def get_product_by_id(self, id_producto: int) -> Producto | None:
        return self.repo.get_product_by_id(id_producto)

    def save_product(self, producto: Producto):
        self.repo.save_product(producto)

    def get_filtered_products(self, buscado: str) -> list[Producto] | list:
        if not buscado:
            return []
        return self.repo.get_filtered(buscado)

    def get_filtered_no_stock(self, buscado: str) -> list[Producto] | list:
        if not buscado:
            return []
        return self.repo.get_filtered_no_stock(buscado)

    def get_products_by_id_list(self, ids_buscadas: list) -> list[Producto] | list:
        if not ids_buscadas:
            return []
        return self.repo.get_products_by_id_list(ids_buscadas)

    def add_stock(self, id_producto: int, cantidad: int):
        self.repo.add_stock(id_producto, cantidad)

    def update_stock(self, id_producto: int, cantidad: int):
        self.repo.update_stock(id_producto, cantidad)

    def update_all_prices(self, percent: int = 0):
        # calcular el multiplicador
        percent_multiplier = round((1 + int(percent) / 100.0), 2)
        # actualizar todos los precios
        self.repo.update_all_prices(percent_multiplier)

    def update_selected_product_prices(self, ids_list: list[int], percent: int = 0):
        if not ids_list:
            return
        percent_multiplier = round((1 + int(percent) / 100.0), 2)
        if percent_multiplier == 0:
            raise ValueError("El multiplicador no puede ser cero.")
        self.repo.update_selected_product_prices(ids_list, percent_multiplier)

    def update_price_to_new_value(self, ids_list: list[int], new_price: str):
        if not ProductoService.validate_price(new_price):
            raise ValueError("Precio inválido.")

        new_price_value = self.transform_price_to_float(new_price)
        self.repo.update_price_to_new_value(ids_list, new_price_value)

    def add_stock_to_multiple_products(self, ids_list: list[int], stock_to_add: int):
        if not ids_list:
            return
        for id_producto in ids_list:
            self.repo.add_stock(id_producto, stock_to_add)

    def update_stock_to_multiple_products(self, ids_list: list[int], new_stock: int):
        if not ids_list:
            return
        self.repo.update_stock_to_multiple_products(ids_list, new_stock)

    def update_product_info(self, id_producto: int, new_info: dict):
        producto = self.repo.get_product_by_id(id_producto)

        #if producto is None:
        #    raise ValueError("Producto no encontrado.")

        # Validaciones
        if 'precio' in new_info and not self.validate_price(new_info['precio']):
            raise ValueError("Precio inválido.")
        if 'stock' in new_info and not self.validate_stock(str(new_info['stock'])):
            raise ValueError("Stock inválido.")

        # Actualizar la información del producto
        for key, value in new_info.items():
            if key == 'precio':
                setattr(producto, key, self.transform_price_to_float(value))
            elif key == 'stock':
                setattr(producto, key, int(value))
            else:
                setattr(producto, key, value)

        # Guardar los cambios en la base de datos
        self.repo.save_product(producto)

    def get_product_name_by_id(self, product_id: int) -> str:
        producto = self.repo.get_product_by_id(product_id)
        if producto is not None:
            return producto.producto
        return 'No encontrado'