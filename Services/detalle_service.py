from Models.detalle_venta import DetalleVenta
from Repositories.detalle_repository import DetalleRepository

class DetalleService:

    def __init__(self):
        self.repo = DetalleRepository()

    @staticmethod
    def create_detalle(cantidad: int, precio_unitario: float, producto_id: int, venta_id: int) -> DetalleVenta:
        if cantidad <= 0:
            raise ValueError('La cantidad en un detalle de venta no puede ser cero o negativa.')
        if precio_unitario < 0:
            raise ValueError('El precio unitario no puede ser negativo.')

        new_detalle = DetalleVenta(cantidad=cantidad, precio_unitario_actual=precio_unitario, id_producto=producto_id, id_venta=venta_id)

        return new_detalle


    def save_detalle(self, detalle: DetalleVenta) -> bool:
        try:
            self.repo.save_detalle(detalle)
            return True
        except Exception as e:
            print(f'Error al guardar el detalle de venta: {e}')
            return False
