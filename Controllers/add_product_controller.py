from Views.add_products_window import AddProductsWindow
from Services.producto_service import ProductoService
from custom_errors import DomainValidationError


class AddProductController:
    def __init__(self, invoqued_by_window):
        self.view_pointer = AddProductsWindow(invoqued_by_window, self)
        self.view_pointer.render_view()
        self.product_service_pointer = ProductoService()
        #self.view.show()

    def add_product(self, product_data):
        try:
            new_product = self.product_service_pointer.create_new_product(
                producto=product_data['producto'],
                codigo=product_data['codigo'],
                precio=product_data['precio'],
                detalle=product_data['detalle'],
                codigo_de_barras=product_data['codigo_de_barras'],
                stock=product_data['stock']
            )
            self.product_service_pointer.save_product(new_product)
            self.view_pointer.show_success_message()

        except DomainValidationError as dve:
            self.view_pointer.show_error_message(str(dve))
        except Exception as e:
            self.view_pointer.show_error_message(f"Error al agregar el producto: {str(e)}")
        
