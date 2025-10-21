from app.infrastructure.database.sqlalchemy.unit_of_work.uow_factory import uow_factory
from app.application.use_cases.add_product import AddProduct
from app.domain.custom_errors import DomainValidationError

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infrastructure.ui.tkinter.views.views.add_product_view import AddProductsView

class AddProductController:
    def __init__(self, view: 'AddProductsView'):

        self.uow_factory = uow_factory
        self.view = view

    def finished_init(self):
        self.view.render_view()

    def add_product(self, product_data):
        for key, value in product_data.items():
            if str(value) == '' or str(value).isspace():
                self.view.show_error("Completá todos los campos")
                return
        try:
            AddProduct(self.uow_factory).execute(
            nombre=product_data['nombre'],
            codigo=product_data['codigo'],
            precio_param=product_data['precio'],
            detalle=product_data['detalle'],
            codigo_de_barras=product_data['codigo_de_barras'],
            stock_param=product_data['stock'])

            self.view.show_success_message()

        except DomainValidationError as dve:
            self.view.show_error_message(str(dve))
        except Exception as e:
            self.view.show_error_message(f"Error al agregar el producto: {str(e)}")
            raise e # TODO añadir logger para guardar el log de los errores


        
