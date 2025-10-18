from dataclasses import dataclass
from decimal import Decimal

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
        entero, decimal = divmod(self.value, 1)
        entero = int(entero)
        decimal = int((decimal * 100).quantize(Decimal("1")))

        return f"${entero:,.0f}".replace(",", ".") + f",{decimal:02d}"
