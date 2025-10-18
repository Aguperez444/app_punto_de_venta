from app.domain.models.precio import Precio
from app.infrastructure.database.sqlalchemy.unit_of_work_impl import UowFactory


class UpdatePrice:
    def __init__(self, uow_factory: UowFactory):
        self.uow_factory = uow_factory

    def update_all(self, percent: str | float = 0.0):
        # calcular el multiplicador
        try:
            percent_multiplier = round((1 + float(percent) / 100.0), 4)
        except ValueError:
            raise ValueError("El porcentaje debe ser un número válido.")

        # actualizar todos los precios
        with self.uow_factory() as uow:
            uow.product_repo.update_all_prices(percent_multiplier)


    def update_selected(self, ids_list: list[int], percent: float = 0.0):
        if not ids_list:
            return
        percent_multiplier = round((1 + float(percent) / 100.0), 4)
        if percent_multiplier == 0:
            raise ValueError("El multiplicador no puede ser cero.")

        with self.uow_factory() as uow:
         uow.product_repo.update_selected_product_prices(ids_list, percent_multiplier)


    def update_to_new_value(self, ids_list: list[int], new_price: str):
        new_price_value = Precio.from_string(new_price)
        with self.uow_factory() as uow:
            uow.product_repo.update_price_to_new_value(ids_list, new_price_value)