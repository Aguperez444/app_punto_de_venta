class DomainValidationError(Exception):
    """Error base para violaciones de reglas e invariantes del dominio."""


class StockInvalidError(DomainValidationError):
    """Error al construir o manipular un valor de stock inválido."""


class PriceInvalidError(DomainValidationError):
    """Error al construir o manipular un precio inválido."""


class NotFoundProductError(DomainValidationError):
    """Error cuando un producto solicitado no existe."""


class VentaNoIdError(DomainValidationError):
    """Error cuando una venta carece de identificador requerido."""


class EmptySaleError(DomainValidationError):
    """Error al intentar confirmar o persistir una venta sin ítems."""


class DatabaseError(Exception):
    """Error técnico de acceso o persistencia en la base de datos."""
