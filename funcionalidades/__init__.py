# importar en init

"""
from .alumnos import (
    listar_alumnos,
    alta_alumno,
    baja_alumno,
    modificar_alumno,
)"""

# importar para asistencia.py

from .asistencia import (
    gestion_asistencias, panel_asistencias, construir_indices, listar_alumnos_ordenados, mostrar_lista_de_clases, mostrar_encabezado_clase, mostrar_tabla_clase, registrar_asistencia_secuencial, modificar_o_eliminar_registro, submenu_filtros, ver_alumnos_global, ver_historial_y_totales_alumno,
)

__all__ = [
"""    # alumnos
    "listar_alumnos", "alta_alumno", "baja_alumno", "modificar_alumno","""
    
    # asistencias
    "gestion_asistencias", "panel_asistencias",
    "construir_indices", "listar_alumnos_ordenados",
    "mostrar_lista_de_clases", "mostrar_encabezado_clase", "mostrar_tabla_clase",
    "registrar_asistencia_secuencial", "modificar_o_eliminar_registro",
    "submenu_filtros", "ver_alumnos_global", "ver_historial_y_totales_alumno",
]
