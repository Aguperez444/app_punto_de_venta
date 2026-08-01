from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from app.application.building_blocks.numeric_base import NumericBase
from app.domain.custom_errors import PriceInvalidError

@dataclass()
class Precio(NumericBase):
    value: Decimal

    def __post_init__(self):
        # Validamos que no sea negativo
        if self.value < Decimal("0"):
            raise PriceInvalidError("El precio no puede ser negativo.")

    @classmethod
    def from_string(cls, precio_param: str) -> "Precio":
        """
        Crea un objeto Price a partir de un string como '$120,50'.
        """
        # Normalizamos el string
        normalized = precio_param.replace('.', '').replace(',', '.').replace('$', '').replace(' ', '').strip()
        try:
            value = Decimal(normalized)
        except Exception as e:
            raise PriceInvalidError(f"Precio inválido: {precio_param}", e)
        return cls(value)

    def __str__(self):
        quantized = self.value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        entero, decimal = divmod(quantized, Decimal("1"))
        centavos = int((decimal * 100).to_integral_value(rounding=ROUND_HALF_UP))

        return f"${int(entero):,}".replace(",", ".") + f",{centavos:02d}"
