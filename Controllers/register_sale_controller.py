from Models.detalle_venta import DetalleVenta
from Services.venta_service import VentaService
from Views.sale_register_window import SalesRegisterWindow
from Services.producto_service import ProductoService
from Services.ACID_transactions import AcidTransaction
from datetime import datetime
from custom_errors import DomainValidationError


class RegisterSaleController:
    def __init__(self, invoqued_by_controller, invoqued_by_window, product_id: int): #TODO REVISAR SI CONTROLLER INVOCA CONTROLLER O WINDOW INVOCA CONTROLLER
        self.parent_controller = invoqued_by_controller
        self.venta_service = VentaService()
        self.product_service = ProductoService()
        self.product_id = product_id
        self.main_window = invoqued_by_window

        self.view = SalesRegisterWindow(invoqued_by_window, self)

        self.view.render_view()


    def show_product_data(self):
        product = self.get_product_data()
        self.view.adjust_product_text(product.producto)
        self.view.pasar_al_cuadro([product])


    def get_product_data(self):
        found = self.product_service.get_product_by_id(self.product_id)
        return found


    def register_new_sale(self, quantity_sold: str):
        product_data = self.get_product_data()
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

        try:
            _precio = float(product_data.precio)
        except ValueError:
            self.view.show_error('El precio del producto no es válido, error inesperado, contacte al administrador.')
            return

        acid_transaction = AcidTransaction()
        try:
            sale_id = acid_transaction.register_sale_ACID(product_data.id, quantity_sold)
            success = True if sale_id else False
        except DomainValidationError as dve:
            self.view.show_error(str(dve))
            return
        except Exception:
            self.view.show_error('Error Desconocido al registrar la venta. Por favor, inténtelo de nuevo.')
            return

        if success:
            self.view.show_message('Venta registrada correctamente.')
            self.main_window.realizar_busqueda()
            self.view.destroy()
        else:
            self.view.show_error('Error al registrar la venta. Por favor, inténtelo de nuevo.')

    @staticmethod
    def get_fecha_hora_actual(_self):
        return datetime.now()

    @staticmethod
    def calculate_total_price(detalles_list: list[DetalleVenta]) -> float:
        return sum(detalle.calcular_subtotal() for detalle in detalles_list)