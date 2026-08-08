from __future__ import annotations

from datetime import datetime

from app.application.ports.clock import IClock


class SystemClock(IClock):
    """Implementación concreta del reloj usando la hora local del sistema."""

    def now(self) -> datetime:
        return datetime.now()
