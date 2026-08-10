"""schema indexes and soft delete

Revision ID: b7c9e2d41a01
Revises: eaaca49ae854
Create Date: 2026-08-10 11:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7c9e2d41a01"
down_revision: Union[str, Sequence[str], None] = "eaaca49ae854"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(inspector: sa.Inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def _column_exists(inspector: sa.Inspector, table_name: str, col_name: str) -> bool:
    return any(col["name"] == col_name for col in inspector.get_columns(table_name))


def _index_exists(inspector: sa.Inspector, table_name: str, idx_name: str) -> bool:
    return any(idx["name"] == idx_name for idx in inspector.get_indexes(table_name))


def upgrade() -> None:
    """Crea tablas faltantes, agrega soft-delete (activo) e índices de consulta."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _table_exists(inspector, "Productos"):
        op.create_table(
            "Productos",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("nombre", sa.String(length=150), nullable=False),
            sa.Column("codigo", sa.String(length=50), nullable=False),
            sa.Column("precio", sa.Numeric(precision=12, scale=2), nullable=False),
            sa.Column("detalle", sa.String(length=255), nullable=True),
            sa.Column("codigo_de_barras", sa.String(length=100), nullable=True),
            sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.CheckConstraint("precio >= 0", name="ck_productos_precio_no_negativo"),
        )
    elif not _column_exists(inspector, "Productos", "activo"):
        op.add_column(
            "Productos",
            sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
        )

    if not _table_exists(inspector, "Ventas"):
        op.create_table(
            "Ventas",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("fecha", sa.DateTime(timezone=False), nullable=False),
            sa.Column("total_price", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0.00"),
            sa.CheckConstraint("total_price >= 0", name="ck_ventas_total_no_negativo"),
        )

    if not _table_exists(inspector, "Detalle_venta"):
        op.create_table(
            "Detalle_venta",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("id_venta", sa.Integer(), sa.ForeignKey("Ventas.id", ondelete="CASCADE"), nullable=False),
            sa.Column("id_producto", sa.Integer(), sa.ForeignKey("Productos.id"), nullable=False),
            sa.Column("cantidad", sa.Integer(), nullable=False),
            sa.Column("precio_unitario_actual", sa.Numeric(precision=12, scale=2), nullable=False),
            sa.CheckConstraint("cantidad > 0", name="ck_detalle_cantidad_positiva"),
            sa.CheckConstraint("precio_unitario_actual >= 0", name="ck_detalle_precio_no_negativo"),
        )

    inspector = sa.inspect(bind)
    indexes = [
        ("Productos", "ix_productos_nombre", ["nombre"]),
        ("Productos", "ix_productos_codigo", ["codigo"]),
        ("Productos", "ix_productos_codigo_de_barras", ["codigo_de_barras"]),
        ("Productos", "ix_productos_stock", ["stock"]),
        ("Productos", "ix_productos_activo", ["activo"]),
        ("Ventas", "ix_ventas_fecha", ["fecha"]),
        ("Detalle_venta", "ix_detalle_venta_id_venta", ["id_venta"]),
        ("Detalle_venta", "ix_detalle_venta_id_producto", ["id_producto"]),
    ]
    for table, idx_name, cols in indexes:
        if _table_exists(inspector, table) and not _index_exists(inspector, table, idx_name):
            op.create_index(idx_name, table, cols)


def downgrade() -> None:
    """Revierte índices y tablas creadas por esta migración."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    indexes = [
        ("Detalle_venta", "ix_detalle_venta_id_producto"),
        ("Detalle_venta", "ix_detalle_venta_id_venta"),
        ("Ventas", "ix_ventas_fecha"),
        ("Productos", "ix_productos_activo"),
        ("Productos", "ix_productos_stock"),
        ("Productos", "ix_productos_codigo_de_barras"),
        ("Productos", "ix_productos_codigo"),
        ("Productos", "ix_productos_nombre"),
    ]
    for table, idx_name in indexes:
        if _table_exists(inspector, table) and _index_exists(inspector, table, idx_name):
            op.drop_index(idx_name, table_name=table)

    if _table_exists(inspector, "Detalle_venta"):
        op.drop_table("Detalle_venta")
    if _table_exists(inspector, "Ventas"):
        op.drop_table("Ventas")
    if _table_exists(inspector, "Productos"):
        op.drop_table("Productos")
