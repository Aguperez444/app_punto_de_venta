from Models.detalle_venta import DetalleVenta
from Services.venta_service import VentaService
from Views.sale_register_window import SalesRegisterWindow
from Services.producto_service import ProductoService
from Services.detalle_service import DetalleService
from Services.ACID_transactions import AcidTransaction
from datetime import datetime
from custom_errors import DomainValidationError


class RegisterSaleController:
    def __init__(self, invoqued_by_controller, invoqued_by_window, product_id: int):
        self.parent_controller = invoqued_by_controller
        self.venta_service = VentaService()
        self.product_service = ProductoService()
        self.detalle_service = DetalleService()
        self.product_id = product_id

        product_data = self.get_product_data()

        print('\n\nproduct_data:', product_data, '\n\n')

        self.view_pointer = SalesRegisterWindow(invoqued_by_window, self, product_data)

        self.view_pointer.render_view()


    def get_product_data(self):
        found = self.product_service.get_product_by_id(self.product_id)
        return found.__dict__


    def register_new_sale(self, product_data: dict, quantity_sold: str):
        try:
            quantity_sold = int(quantity_sold)
            if quantity_sold <= 0:
                raise DomainValidationError('La cantidad vendida debe ser un número positivo.')
        except DomainValidationError as dve:
            self.view_pointer.show_error(str(dve))
            return
        except ValueError:
            self.view_pointer.show_error('La cantidad vendida debe ser un número entero válido, no se aceptan letras o símbolos.')
            return

        try:
            _precio = float(product_data['precio'])
        except Exception:
            self.view_pointer.show_error('El precio del producto no es válido.')
            return

        acid_transaction = AcidTransaction()
        try:
            sale_id = acid_transaction.register_sale_ACID(product_data['id'], quantity_sold)
            success = True if sale_id else False
        except DomainValidationError as dve:
            self.view_pointer.show_error(str(dve))
            return
        except Exception:
            self.view_pointer.show_error('Error Desconocido al registrar la venta. Por favor, inténtelo de nuevo.')
            return

        if success:
            self.view_pointer.sale_registered()
        else:
            self.view_pointer.show_error('Error al registrar la venta. Por favor, inténtelo de nuevo.')

    @staticmethod
    def get_fecha_hora_actual(_self):
        return datetime.now()

    @staticmethod
    def calculate_total_price(detalles_list: list[DetalleVenta]) -> float:
        return sum(detalle.calcular_subtotal() for detalle in detalles_list)