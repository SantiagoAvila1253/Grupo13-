# Exposición controlada de la API de core

# Submódulos (para: from core import es_json, es_csv, validadores, helpers, estadisticas, menus)
from . import es_json
from . import es_csv
from . import validadores
from . import helpers
from . import estadisticas
from . import menus
from . import datos

# Re-export de funciones puntuales para “imports cortos” desde app_presentismo.py
from .menus import (
    mostrar_menu_login,
    mostrar_menu_principal,
    mostrar_menu_alumnos,
    mostrar_menu_asistencia,
    mostrar_menu_reportes,
    mostrar_menu_filtrar,
)
from .validadores import (
    opcion_valida_menu,
    dni_valido,
    nom_ape_valido,
    email_valido,
    password_valida,
    fecha_ddmmaaaa_valida,
    validar_numero_entero,
    validar_numero_positivo,
    validar_legajo_formato,
    validar_id_clase_formato,
    validar_legajo_existente,
    validar_id_clase_existente,
    validar_estado_asistencia,
    validar_fila_csv,
)

# Alias de compatibilidad: lo que antes llamaban “legajo_valido”
# Usa el helper real para pedir un legajo existente
from .helpers import pedir_legajo_existente as legajo_valido

# Constantes del sistema (para consumir directo desde core si las necesitan)
from .datos import (
    ESTADOS_ASISTENCIA,
    PRESENTE, AUS_J, AUS_I,
    AL_ACTIVO, AL_INACTIVO,
    CABECERA_CSV, CSV_SEP,
    PORC_MAX_INASISTENCIA, DECIMALES_PORCENTAJE,
    ID_DOCENTE_INICIAL, ID_CLASE_INICIAL, ID_ALUMNO_INICIAL,
)

__all__ = [
    # submódulos
    "es_json", "es_csv", "validadores", "helpers", "estadisticas", "menus", "datos",
    # menús
    "mostrar_menu_login", "mostrar_menu_principal", "mostrar_menu_alumnos",
    "mostrar_menu_asistencia", "mostrar_menu_reportes", "mostrar_menu_filtrar",
    # validadores
    "opcion_valida_menu", "dni_valido", "nom_ape_valido", "email_valido",
    "password_valida", "fecha_ddmmaaaa_valida", "validar_numero_entero",
    "validar_numero_positivo", "validar_legajo_formato", "validar_id_clase_formato",
    "validar_legajo_existente", "validar_id_clase_existente",
    "validar_estado_asistencia", "validar_fila_csv",
    # helpers
    "legajo_valido",
    # datos
    "ESTADOS_ASISTENCIA", "PRESENTE", "AUS_J", "AUS_I",
    "AL_ACTIVO", "AL_INACTIVO",
    "CABECERA_CSV", "CSV_SEP",
    "PORC_MAX_INASISTENCIA", "DECIMALES_PORCENTAJE",
    "ID_DOCENTE_INICIAL", "ID_CLASE_INICIAL", "ID_ALUMNO_INICIAL",
]
