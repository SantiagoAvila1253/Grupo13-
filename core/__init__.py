from .datos import (
    ESTADOS_ASISTENCIA, ESTADOS_ALUMNO,
    DOCENTES, CLASES,
    alumnos, DO_LEGAJO, DO_DNI, DO_CLAVE, DO_NOMBRE, DO_APELLIDO, DO_EMAIL,
    AL_LEGAJO, AL_DNI, AL_EMAIL, AL_APELLIDO, AL_NOMBRE, AL_ESTADO,
    CL_ID, CL_MATERIA, CL_FECHA, CL_DIA, CL_HORARIO,
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
    # datos
    "ESTADOS_ASISTENCIA","ESTADOS_ALUMNO","DOCENTES","CLASES","alumnos",
    "DO_LEGAJO","DO_DNI","DO_CLAVE","DO_NOMBRE","DO_APELLIDO","DO_EMAIL",
    "AL_LEGAJO","AL_DNI","AL_EMAIL","AL_APELLIDO","AL_NOMBRE","AL_ESTADO",
    "CL_ID","CL_MATERIA","CL_FECHA","CL_DIA","CL_HORARIO",
    "PR_CLASE_IDX","PR_ALUMNO_LEGAJO","PR_ESTADO_ASIST_IDX","PR_ESTADO_ALUMNO_IDX",
    # menus
    "mostrar_menu_login","mostrar_menu_principal","mostrar_menu_alumnos",
    "mostrar_menu_asistencia","mostrar_menu_reportes",
    # validadores
    "opcion_valida_menu","dni_valido","legajo_valido","email_valido",
    "nombre_valido","apellido_valido","fecha_ddmmyyyy_valida","password_valida",
]
