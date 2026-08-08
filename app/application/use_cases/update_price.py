from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from app.application.ports.unit_of_work import UowFactory
from app.domain.models.precio import Precio


class UpdatePrice:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    @staticmethod
    def _parse_multiplier(percent: str | int | float | Decimal) -> Decimal:
        raw = str(percent).strip().replace(",", ".")
        try:
            pct = Decimal(raw)
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("El porcentaje debe ser un número válido.") from exc

        multiplier = (Decimal("1") + (pct / Decimal("100"))).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )
        if multiplier <= Decimal("0"):
            raise ValueError("El porcentaje debe ser mayor a -100% (el multiplicador debe ser positivo).")
        return multiplier

    def update_all(self, percent: str | int | float | Decimal = Decimal("0")) -> None:
        percent_multiplier = self._parse_multiplier(percent)

        with self.uow_factory() as uow:
            uow.product_repo.update_all_prices(percent_multiplier)
            uow.commit()

    def update_selected(
        self, ids_list: list[int], percent: str | int | float | Decimal = Decimal("0")
    ) -> None:
        if not ids_list:
            return
        percent_multiplier = self._parse_multiplier(percent)

        with self.uow_factory() as uow:
            uow.product_repo.update_selected_product_prices(ids_list, percent_multiplier)
            uow.commit()

    def update_to_new_value(self, ids_list: list[int], new_price: str) -> None:
        if not ids_list:
            return
        new_price_value = Precio.from_string(new_price)
        with self.uow_factory() as uow:
            uow.product_repo.update_price_to_new_value(ids_list, new_price_value)
            uow.commit()
