# importar en init

from .datos import (
    # importar listas fijas
    ESTADOS_ASISTENCIA, ESTADOS_ALUMNO, PRESENTE, AUS_J, AUS_I, AL_ACTIVO, AL_INACTIVO,


)

from .menus import (
    mostrar_menu_login, mostrar_menu_principal, mostrar_menu_alumnos, mostrar_menu_asistencia, mostrar_menu_reportes, mostrar_submenu_filtrar
)

from .validadores import (
    opcion_valida_menu, dni_valido, estado_asistencia_valido, email_valido, password_valida, nom_ape_valido, fecha_ddmmaaaa_valida
)

from .helpers import (
    legajo_valido, actualizar_alumnos_ordenada
)

__all__ = [
    # importar listas fijas
    "ESTADOS_ASISTENCIA", "ESTADOS_ALUMNO", "PRESENTE", "AUS_J", "AUS_I", "AL_ACTIVO", "AL_INACTIVO",

    # docentes + referencias
    "docentes", "DO_LEGAJO", "DO_DNI", "DO_CLAVE", "DO_NOMBRE", "DO_APELLIDO", "DO_EMAIL",

    # clases + referencias
    "clases", "CL_ID", "CL_MATERIA", "CL_FECHA", "CL_DIA", "CL_HORARIO",

    # alumnos + referencias
    "alumnos", "AL_LEGAJO", "AL_DNI", "AL_APELLIDO", "AL_NOMBRE", "AL_FECHA_NAC", "AL_EMAIL", "AL_ESTADO",
    "alumnos_ordenada", "alumnos_baja",

    # asistencias
    "asistencias",

    # menús
    "mostrar_menu_login", "mostrar_menu_principal", "mostrar_menu_alumnos", "mostrar_menu_asistencia", "mostrar_menu_reportes", "mostrar_submenu_filtrar",

    # validadores
    "opcion_valida_menu", "dni_valido", "estado_asistencia_valido", "email_valido", "nom_ape_valido", "fecha_ddmmaaaa_valida", "password_valida",
    
    # helpers
    "legajo_valido", "actualizar_alumnos_ordenada"
]
