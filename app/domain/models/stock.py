from dataclasses import dataclass

from app.application.building_blocks.numeric_base import NumericBase
from app.domain.custom_errors import StockInvalidError


@dataclass()
class Stock(NumericBase):
    value: int


    @classmethod
    def from_string(cls, stock_param: str) -> "Stock":
        """
        Crea un objeto Stock a partir de un string como '15'.
        """
        try:
            value = int(stock_param)
        except ValueError:
            raise StockInvalidError(f"El valor del stock no es válido: {stock_param}")
        return cls(value)

    def __str__(self):
        return f'{self.value}'