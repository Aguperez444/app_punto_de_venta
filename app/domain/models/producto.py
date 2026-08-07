from __future__ import annotations

from app.domain.custom_errors import DomainValidationError
from app.domain.models.precio import Precio
from app.domain.models.stock import Stock


class Producto:
    def __init__(
        self,
        id_producto: int | None,
        nombre: str,
        codigo: str,
        precio: Precio,
        detalle: str | None,
        codigo_de_barras: str | None,
        stock: Stock,
        activo: bool = True,
    ):
        nombre_limpio = (nombre or "").strip()
        codigo_limpio = (codigo or "").strip()
        if not nombre_limpio:
            raise DomainValidationError("El nombre del producto no puede estar vacío.")
        if not codigo_limpio:
            raise DomainValidationError("El código del producto no puede estar vacío.")

        self._id_producto = id_producto
        self._nombre = nombre_limpio
        self._codigo = codigo_limpio
        self._precio = precio
        self._detalle = (detalle or "").strip()
        self._codigo_de_barras = (codigo_de_barras or "").strip()
        self._stock = stock
        self._activo = bool(activo)

    def disminuir_stock(self, amount: int) -> None:
        """Resta stock al registrar una venta. Permite stock negativo por regla de negocio."""
        if amount < 0:
            raise ValueError("El valor de stock a restar debe ser mayor o igual a 0")
        self._stock = self._stock - Stock(amount)

    def ajustar_stock(self, delta: int) -> None:
        """Ajusta el stock en forma positiva o negativa."""
        self._stock = self._stock + Stock(delta)

    def desactivar(self) -> None:
        self._activo = False

    def reactivar(self) -> None:
        self._activo = True

    @classmethod
    def from_string(
        cls,
        nombre: str,
        codigo: str,
        precio_param: str,
        detalle: str | None,
        codigo_de_barras: str | None,
        stock_param: str,
        activo: bool = True,
    ) -> "Producto":
        precio = Precio.from_string(precio_param)
        stock = Stock.from_string(stock_param)

        return cls(
            id_producto=None,
            nombre=nombre,
            codigo=codigo,
            precio=precio,
            detalle=detalle,
            codigo_de_barras=codigo_de_barras,
            stock=stock,
            activo=activo,
        )

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def id_producto(self) -> int | None:
        return self._id_producto

    @id_producto.setter
    def id_producto(self, value: int | None) -> None:
        self._id_producto = value

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def precio(self) -> Precio:
        return self._precio

    @property
    def detalle(self) -> str:
        return self._detalle

    @property
    def codigo_de_barras(self) -> str:
        return self._codigo_de_barras

    @property
    def stock(self) -> Stock:
        return self._stock

    @property
    def activo(self) -> bool:
        return self._activo

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return NotImplemented
        return (
            self._id_producto == other._id_producto
            and self._nombre == other._nombre
            and self._codigo == other._codigo
            and self._precio == other._precio
            and self._detalle == other._detalle
            and self._codigo_de_barras == other._codigo_de_barras
            and self._stock == other._stock
            and self._activo == other._activo
        )

    def __repr__(self) -> str:
        return (
            f"Producto(id={self._id_producto!r}, nombre={self._nombre!r}, "
            f"codigo={self._codigo!r}, precio={self._precio}, stock={self._stock}, activo={self._activo})"
        )
