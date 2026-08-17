from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from app.application.use_cases.register_sale import SaleItemInput
from app.domain.models.precio import Precio
from app.domain.models.producto import Producto


@dataclass
class CartLine:
    producto: Producto
    cantidad: int

    @property
    def subtotal(self) -> Decimal:
        return (Decimal(self.cantidad) * self.producto.precio.value).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def subtotal_precio(self) -> Precio:
        return Precio(self.subtotal)


class SaleCart:
    """
    Estado en memoria del carrito de ventas de mostrador.
    - Cuando está vacío, el flujo rápido (Enter -> Enter) registra la venta directa de 1 producto.
    - Una vez que contiene al menos 1 ítem, la acción por defecto pasa a ser 'Añadir al carrito'.
    """

    def __init__(self) -> None:
        self._lines: dict[int, CartLine] = {}

    @property
    def is_empty(self) -> bool:
        return len(self._lines) == 0

    @property
    def has_items(self) -> bool:
        return not self.is_empty

    @property
    def items_count(self) -> int:
        return len(self._lines)

    @property
    def total_units(self) -> int:
        return sum(line.cantidad for line in self._lines.values())

    @property
    def total(self) -> Precio:
        total_dec = sum((line.subtotal for line in self._lines.values()), Decimal("0.00"))
        return Precio(total_dec.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    @property
    def lines(self) -> list[CartLine]:
        return list(self._lines.values())

    def add_item(self, producto: Producto, cantidad: int = 1) -> CartLine:
        if producto.id_producto is None:
            raise ValueError("El producto debe tener un ID válido para agregarse al carrito.")
        if cantidad <= 0:
            raise ValueError("La cantidad a agregar al carrito debe ser mayor a 0.")

        if producto.id_producto in self._lines:
            line = self._lines[producto.id_producto]
            line.cantidad += cantidad
            line.producto = producto
            return line

        line = CartLine(producto=producto, cantidad=cantidad)
        self._lines[producto.id_producto] = line
        return line

    def update_quantity(self, product_id: int, new_cantidad: int) -> None:
        if product_id not in self._lines:
            return
        if new_cantidad <= 0:
            del self._lines[product_id]
        else:
            self._lines[product_id].cantidad = new_cantidad

    def remove_item(self, product_id: int) -> None:
        self._lines.pop(product_id, None)

    def clear(self) -> None:
        self._lines.clear()

    def to_sale_items(self) -> list[SaleItemInput]:
        return [
            SaleItemInput(product_id=pid, amount=line.cantidad)
            for pid, line in self._lines.items()
        ]
