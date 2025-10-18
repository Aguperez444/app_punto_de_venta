from app.domain.models.detalle_venta import DetalleVenta

from app.infrastructure.database.sqlalchemy.uow_factory import uow_factory

from app.application.use_cases.query_products import QueryProducts
from app.application.use_cases.register_sale import RegisterSale

from app.infrastructure.ui.tkinter.views.popups.sale_register_popup import SalesRegisterWindow
from datetime import datetime
from app.domain.custom_errors import DomainValidationError


class RegisterSaleController:
    def __init__(self, invoked_by_controller, invoked_by_window, product_id: int):
        self.parent_controller = invoked_by_controller

        self.product_id = product_id
        self.main_window = invoked_by_window
        self.uow_factory = uow_factory

        self.view = SalesRegisterWindow(invoked_by_window, self)

        self.view.render_view()


    def show_product_data(self):
        product = self.get_product_data()
        self.view.adjust_product_text(product.nombre)
        self.view.pasar_al_cuadro([product])


    def get_product_data(self):
        found = QueryProducts(self.uow_factory).get_by_id(self.product_id)
        return found


    def register_new_sale(self, quantity_sold: str):
        try:
            quantity_sold = int(quantity_sold)
            if quantity_sold <= 0:
                raise DomainValidationError('La cantidad vendida debe ser un número positivo.')
        except DomainValidationError as dve:
            self.view.show_error(str(dve))
            return
        except ValueError:
            self.view.show_error('La cantidad vendida debe ser un número entero válido, no se aceptan letras o símbolos.')
            return

        product_data = self.get_product_data()

        try:
            date = self.get_fecha_hora_actual()
            sale_id = RegisterSale(self.uow_factory).execute(product_data.id_producto, quantity_sold, date)
            success = True if sale_id else False
        except DomainValidationError as dve:
            self.view.show_error(str(dve))
            return
        except Exception as e:
            self.view.show_error(f'Error Desconocido al registrar la venta. Por favor,'
                                 f' contacte al administrador del sistema {str(e)}')
            raise e #TODO implementar logger de errores donde se guarde la exception capturada

        if success:
            self.view.show_message('Venta registrada correctamente.')
            self.main_window.realizar_busqueda()
            self.view.destroy()
        else:
            self.view.show_error('Error al registrar la venta. Por favor, inténtelo de nuevo.')

    @staticmethod
    def get_fecha_hora_actual():
        return datetime.now()

    @staticmethod
    def calculate_total_price(detalles_list: list[DetalleVenta]) -> float:
        return sum(detalle.calcular_subtotal() for detalle in detalles_list)