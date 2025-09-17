from datetime import datetime
from Models.DetalleVenta import DetalleVenta
from Models.Producto import Producto
from Models.Venta import Venta
from Database.db_session import SessionLocal
from custom_errors import DomainValidationError


class AcidTransaction:
    def __init__(self):
        pass

    @staticmethod
    def register_sale_ACID(product_id: int, cantidad: int) -> int:
        with SessionLocal() as session:
            try:
                now = datetime.now()
                venta = Venta(fecha=now, total_price=0)
                session.add(venta)
                session.flush()

                producto = session.get(Producto, product_id)
                if producto is None: raise DomainValidationError("Producto inexistente")

                detalle = DetalleVenta(
                    id_venta=venta.id,
                    id_producto=product_id,
                    cantidad=cantidad,
                    precio_unitario_actual=float(producto.precio)
                )
                session.add(detalle)

                venta.total_price = detalle.calcular_subtotal()
                producto.stock -= cantidad

                session.commit()
                return venta.id
            except:
                session.rollback()
                raise