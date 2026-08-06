from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from app.domain.custom_errors import PriceInvalidError


@dataclass(frozen=True)
class Precio:
    value: Decimal

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, (Decimal, int)):
            raise PriceInvalidError(f"Tipo de precio inválido: {type(self.value).__name__}")
        dec_value = Decimal(self.value) if not isinstance(self.value, Decimal) else self.value
        if dec_value.is_nan() or dec_value.is_infinite():
            raise PriceInvalidError("El precio debe ser un número finito.")
        if dec_value < Decimal("0"):
            raise PriceInvalidError("El precio no puede ser negativo.")
        object.__setattr__(self, "value", dec_value)

    @classmethod
    def from_string(cls, precio_param: str) -> "Precio":
        """Crea un objeto Precio a partir de un string como '$1.234,50' o '120,50'."""
        if not isinstance(precio_param, str):
            raise PriceInvalidError(f"Precio inválido: {precio_param}")
        raw = precio_param.replace("$", "").replace(" ", "").strip()
        if not raw:
            raise PriceInvalidError(f"Precio inválido: {precio_param}")

        # Soporta formato es-AR ('1.234,56') y decimal con punto ('1234.56')
        if "," in raw:
            normalized = raw.replace(".", "").replace(",", ".")
        elif raw.count(".") == 1:
            entero, dec = raw.split(".")
            if len(dec) == 3 and entero.isdigit() and dec.isdigit() and len(entero) >= 1 and int(entero) > 0:
                # Ej: "1.500" interpretado como mil quinientos si no hay coma
                normalized = entero + dec
            else:
                normalized = raw
        else:
            normalized = raw.replace(".", "")

        try:
            value = Decimal(normalized)
        except (InvalidOperation, ValueError) as e:
            raise PriceInvalidError(f"Precio inválido: {precio_param}") from e
        return cls(value)

    def aplicar_porcentaje(self, percent: Decimal) -> "Precio":
        multiplier = Decimal("1") + (Decimal(percent) / Decimal("100"))
        if multiplier <= Decimal("0"):
            raise PriceInvalidError("El porcentaje resulta en un precio menor o igual a cero.")
        new_value = (self.value * multiplier).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return Precio(new_value)

    def __add__(self, other: object) -> "Precio":
        if isinstance(other, Precio):
            return Precio(self.value + other.value)
        if isinstance(other, (Decimal, int)) and not isinstance(other, bool):
            return Precio(self.value + Decimal(other))
        return NotImplemented

    def __radd__(self, other: object) -> "Precio":
        if other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other: object) -> "Precio":
        if isinstance(other, Precio):
            return Precio(self.value - other.value)
        if isinstance(other, (Decimal, int)) and not isinstance(other, bool):
            return Precio(self.value - Decimal(other))
        return NotImplemented

    def __mul__(self, other: object) -> "Precio":
        if isinstance(other, (Decimal, int)) and not isinstance(other, bool):
            return Precio(self.value * Decimal(other))
        return NotImplemented

    def __rmul__(self, other: object) -> "Precio":
        return self.__mul__(other)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Precio):
            return self.value < other.value
        if isinstance(other, (Decimal, int)) and not isinstance(other, bool):
            return self.value < Decimal(other)
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, Precio):
            return self.value <= other.value
        if isinstance(other, (Decimal, int)) and not isinstance(other, bool):
            return self.value <= Decimal(other)
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Precio):
            return self.value > other.value
        if isinstance(other, (Decimal, int)) and not isinstance(other, bool):
            return self.value > Decimal(other)
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Precio):
            return self.value >= other.value
        if isinstance(other, (Decimal, int)) and not isinstance(other, bool):
            return self.value >= Decimal(other)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Precio):
            return self.value == other.value
        if isinstance(other, (Decimal, int)) and not isinstance(other, bool):
            return self.value == Decimal(other)
        return NotImplemented

    def __str__(self) -> str:
        quantized = self.value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        entero, decimal = divmod(quantized, Decimal("1"))
        centavos = int((decimal * 100).to_integral_value(rounding=ROUND_HALF_UP))
        return f"${int(entero):,}".replace(",", ".") + f",{centavos:02d}"
