# __init__.py dentro de funcionalidades

from .alumnos import menu_alumnos
from .reportes import menu_reportes
from .asistencia import gestion_asistencias
from .filtros import menu_filtros

__all__ = [
    "menu_alumnos",
    "menu_reportes",
    "gestion_asistencias",
    "menu_filtros",
]
