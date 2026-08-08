from __future__ import annotations

from datetime import datetime
from typing import Protocol


class IClock(Protocol):
    """Puerto para obtener la fecha y hora actual de forma desacoplada y testeable."""

    def now(self) -> datetime:
        ...
