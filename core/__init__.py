# Re-exporto para importar desde 'core' directo
from .datos import (
    ESTADOS_ASISTENCIA, ESTADOS_ALUMNO,
    DOCENTES, MATERIAS, CLASES,
    alumnos, DO_DNI, DO_CLAVE, MA_NOMBRE, MA_DIA, MA_HORARIO,
    AL_LEGAJO, AL_DNI, AL_EMAIL, AL_APELLIDO, AL_NOMBRE, AL_ESTADO_IDX,
    PR_MATERIA_IDX, PR_CLASE_IDX, PR_ALUMNO_LEGAJO, PR_ESTADO_ASIST_IDX, PR_ESTADO_ALUMNO_IDX,
)
from .menus import (
    mostrar_menu_login, mostrar_menu_principal,
    mostrar_menu_alumnos, mostrar_menu_asistencia, mostrar_menu_reportes
)
from .validadores import (
    opcion_valida_menu, dni_valido, legajo_valido, email_valido,
    nombre_valido, apellido_valido, fecha_ddmmyyyy_valida, password_valida
)

__all__ = [
    # data
    "ESTADOS_ASISTENCIA","ESTADOS_ALUMNO","DOCENTES","MATERIAS","CLASES","alumnos",
    "DO_DNI","DO_CLAVE","MA_NOMBRE","MA_DIA","MA_HORARIO",
    "AL_LEGAJO","AL_DNI","AL_EMAIL","AL_APELLIDO","AL_NOMBRE","AL_ESTADO_IDX",
    "PR_MATERIA_IDX","PR_CLASE_IDX","PR_ALUMNO_LEGAJO","PR_ESTADO_ASIST_IDX","PR_ESTADO_ALUMNO_IDX",
    # menus
    "mostrar_menu_login","mostrar_menu_principal","mostrar_menu_alumnos",
    "mostrar_menu_asistencia","mostrar_menu_reportes",
    # validators
    "opcion_valida_menu","dni_valido","legajo_valido","email_valido",
    "nombre_valido","apellido_valido","fecha_ddmmyyyy_valida","password_valida",
]
