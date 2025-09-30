# importar en init
from .alumnos import (menu_alumnos)
from .asistencia import (gestion_asistencias)
from .reportes import (menu_reportes)

__all__ = [
    "menu_alumnos",
    "gestion_asistencias",
    "menu_reportes",
]
