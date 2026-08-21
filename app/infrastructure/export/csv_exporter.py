from __future__ import annotations

import csv
from pathlib import Path

from app.application.dto.sales_dto import SaleDetailDTO
from app.domain.models.producto import Producto
from app.domain.models.venta import Venta


class CsvExporter:
    """Exporta listados de ventas y productos faltantes a archivos CSV compatibles con Excel."""

    @staticmethod
    def export_sales(ventas: list[Venta], output_path: Path | str) -> Path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "wt", encoding="utf-8-sig", newline="") as fh:
            writer = csv.writer(fh, delimiter=";")
            writer.writerow(
                [
                    "ID Venta",
                    "Fecha",
                    "Hora",
                    "Producto",
                    "Código",
                    "Cantidad",
                    "Precio Unitario",
                    "Subtotal",
                    "Total Venta",
                ]
            )
            for venta in ventas:
                detail = SaleDetailDTO.from_domain(venta)
                if not detail.items:
                    writer.writerow(
                        [
                            detail.venta_id or "",
                            detail.fecha_str,
                            detail.hora_str,
                            "(Sin ítems)",
                            "",
                            0,
                            "0.00",
                            "0.00",
                            f"{detail.total:.2f}",
                        ]
                    )
                    continue
                for item in detail.items:
                    writer.writerow(
                        [
                            detail.venta_id or "",
                            detail.fecha_str,
                            detail.hora_str,
                            item.producto_nombre,
                            item.producto_codigo,
                            item.cantidad,
                            f"{item.precio_unitario:.2f}",
                            f"{item.subtotal:.2f}",
                            f"{detail.total:.2f}",
                        ]
                    )
        return target

    @staticmethod
    def export_products(products: list[Producto], output_path: Path | str) -> Path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "wt", encoding="utf-8-sig", newline="") as fh:
            writer = csv.writer(fh, delimiter=";")
            writer.writerow(
                ["ID", "Nombre", "Código", "Precio", "Detalle", "Código de barras", "Stock"]
            )
            for prod in products:
                writer.writerow(
                    [
                        prod.id_producto or "",
                        prod.nombre,
                        prod.codigo,
                        f"{prod.precio.value:.2f}",
                        prod.detalle,
                        prod.codigo_de_barras,
                        prod.stock.value,
                    ]
                )
        return target
