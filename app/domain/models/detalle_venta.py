from decimal import Decimal

from app.domain.models.precio import Precio
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.domain.models.venta import Venta
    from app.domain.models.producto import Producto

class DetalleVenta:
    def __init__(self, id_detalle: int | None, producto_id: int, venta_id: int, cantidad: int,
                 precio_unitario_actual: Precio, product: 'Producto | None' = None, venta: 'Venta | None' = None):
        self._id = id_detalle
        self._venta_id = venta_id
        self._producto_id = producto_id
        self._cantidad = cantidad
        self._precio_unitario_actual = precio_unitario_actual

        #No necesariamente se crean los detalles con el puntero a los objetos productos y ventas, pero sí o sí con el ID
        self.producto = product
        self.venta = venta


    def calcular_subtotal(self) -> Decimal:
        subtotal = Decimal(self._cantidad) * self._precio_unitario_actual.value
        return subtotal.quantize(Decimal('0.01'), rounding='ROUND_HALF_UP')

    @classmethod
    def create_new(cls, producto_id: int, cantidad: int, precio_unitario: Precio, venta_id: int | None = None):
        if cantidad <= 0: raise ValueError("Cantidad ≤ 0 No es válida")
        if precio_unitario.value < 0: raise ValueError("Precio unitario negativo")
        return cls(None, producto_id, venta_id, cantidad, precio_unitario)

    @property
    def id(self):
        return self._id

    @property
    def venta_id(self):
        return self._venta_id

    @property
    def producto_id(self):
        return self._producto_id

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio_unitario_actual(self):
        return self._precio_unitario_actual