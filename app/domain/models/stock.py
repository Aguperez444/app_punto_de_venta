from __future__ import annotations

from dataclasses import dataclass

from app.domain.custom_errors import StockInvalidError


@dataclass(frozen=True)
class Stock:
    """Value Object de stock. Permite valores negativos por regla de negocio (ventas previas a carga)."""

    value: int

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, int):
            raise StockInvalidError(f"El valor del stock debe ser un entero: {self.value!r}")

    @classmethod
    def from_string(cls, stock_param: str) -> "Stock":
        """Crea un objeto Stock a partir de un string como '15' o '-2'."""
        if not isinstance(stock_param, str):
            raise StockInvalidError(f"El valor del stock no es válido: {stock_param}")
        cleaned = stock_param.strip()
        try:
            value = int(cleaned)
        except ValueError as e:
            raise StockInvalidError(f"El valor del stock no es válido: {stock_param}") from e
        return cls(value)

    def __add__(self, other: object) -> "Stock":
        if isinstance(other, Stock):
            return Stock(self.value + other.value)
        if isinstance(other, int) and not isinstance(other, bool):
            return Stock(self.value + other)
        return NotImplemented

    def __radd__(self, other: object) -> "Stock":
        return self.__add__(other)

    def __sub__(self, other: object) -> "Stock":
        if isinstance(other, Stock):
            return Stock(self.value - other.value)
        if isinstance(other, int) and not isinstance(other, bool):
            return Stock(self.value - other)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Stock):
            return self.value < other.value
        if isinstance(other, int) and not isinstance(other, bool):
            return self.value < other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, Stock):
            return self.value <= other.value
        if isinstance(other, int) and not isinstance(other, bool):
            return self.value <= other
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Stock):
            return self.value > other.value
        if isinstance(other, int) and not isinstance(other, bool):
            return self.value > other
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Stock):
            return self.value >= other.value
        if isinstance(other, int) and not isinstance(other, bool):
            return self.value >= other
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Stock):
            return self.value == other.value
        if isinstance(other, int) and not isinstance(other, bool):
            return self.value == other
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.value}"
