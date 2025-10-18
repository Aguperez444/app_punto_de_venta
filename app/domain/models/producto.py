from app.domain.models.precio import Precio
from app.domain.models.stock import Stock


class Producto:
    def __init__(self, id_producto: int | None, nombre: str, codigo: str, precio: Precio,
                 detalle: str, codigo_de_barras: str, stock: Stock):
        self._id_producto = id_producto
        self._nombre = nombre
        self._codigo = codigo
        self._precio = precio
        self._detalle = detalle
        self._codigo_de_barras = codigo_de_barras
        self._stock = stock


    def disminuir_stock(self, amount: int) -> None:
        if amount < 0: raise ValueError('El valor de stock a restar debe ser mayor o igual a 0')
        self._stock -= Stock(amount)


    @classmethod
    def from_string(cls, nombre: str, codigo: str, precio_param: str,
                           detalle: str, codigo_de_barras: str, stock_param: str) -> 'Producto':

        # válida a la vez que crea los objetos de valor
        precio = Precio.from_string(precio_param)
        stock = Stock.from_string(stock_param)

        # crear y retornar objeto producto
        return cls(
            id_producto=None,
            nombre=nombre,
            codigo=codigo,
            precio=precio,
            detalle=detalle,
            codigo_de_barras=codigo_de_barras,
            stock=stock
        )



    @property
    def nombre(self):
        return self._nombre

    @property
    def id_producto(self):
        return self._id_producto

    @id_producto.setter
    def id_producto(self, value):
        self._id_producto = value

    @property
    def codigo(self):
        return self._codigo

    @property
    def precio(self):
        return self._precio

    @property
    def detalle(self):
        return self._detalle

    @property
    def codigo_de_barras(self):
        return self._codigo_de_barras

    @property
    def stock(self):
        return self._stock

