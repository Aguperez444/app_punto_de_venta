from dataclasses import dataclass
from typing import Union
from decimal import Decimal

Numeric = Union[int, float, Decimal]

@dataclass
class NumericBase:
    value: Numeric

    def __add__(self, other):
        if isinstance(other, NumericBase):
            return self.__class__(self.value + other.value)
        elif isinstance(other, Numeric):
            return self.__class__(self.value + other)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, NumericBase):
            return self.__class__(self.value - other.value)
        elif isinstance(other, Numeric):
            return self.__class__(self.value - other)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Numeric):
            return self.__class__(other - self.value)
        return NotImplemented

    # ----- MULTIPLICACIÓN -----
    def __mul__(self, other):
        if isinstance(other, NumericBase):
            return self.__class__(self.value * other.value)
        elif isinstance(other, Numeric):
            return self.__class__(self.value * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    # ----- DIVISIÓN -----
    def __truediv__(self, other):
        if isinstance(other, NumericBase):
            return self.__class__(self.value / other.value)
        elif isinstance(other,Numeric):
            return self.__class__(self.value / other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Numeric):
            return self.__class__(other / self.value)
        return NotImplemented

    # ----- COMPARACIONES -----
    def __eq__(self, other):
        if isinstance(other, NumericBase):
            return self.value == other.value
        elif isinstance(other, Numeric):
            return self.value == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, NumericBase):
            return self.value < other.value
        elif isinstance(other, Numeric):
            return self.value < other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, NumericBase):
            return self.value <= other.value
        elif isinstance(other, Numeric):
            return self.value <= other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, NumericBase):
            return self.value > other.value
        elif isinstance(other, Numeric):
            return self.value > other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, NumericBase):
            return self.value >= other.value
        elif isinstance(other, Numeric):
            return self.value >= other
        return NotImplemented