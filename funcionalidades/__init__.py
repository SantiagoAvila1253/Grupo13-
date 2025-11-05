# __init__.py dentro de funcionalidades

<<<<<<< Updated upstream
from . import asistencia
from . import alumnos
from . import filtros
from . import Reportes
=======
from .alumnos import menu_alumnos
from .reportes import menu_reportes
from .asistencia import gestion_asistencias
from .filtros import menu_filtros
>>>>>>> Stashed changes

__all__ = [
<<<<<<< Updated upstream
    "asistencia",
    "alumnos",
    "filtros",
    "Reportes",
=======
    "menu_alumnos",
    "menu_reportes",
    "gestion_asistencias",
    "menu_filtros",
>>>>>>> Stashed changes
]
