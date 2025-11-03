# Base de datos
"""
Este módulo que antes contenía la base de datos, ahora define constantes y configuraciones globales.
- Se mantiene el uso de tuplas para representar estructuras inmutables
- Archivos persistentes pasan a almacenarse en:
    + data/alumnos.json   -> Diccionario de diccionarios
    + data/clases.json    -> Diccionario de diccionarios
    + data/docentes.json  -> Diccionario de diccionarios
    + data/asistencia.csv -> Matriz (lista de listas)
"""

# Estados de asistencia
ESTADOS_ASISTENCIA = ("Presente", "Ausente justificado", "Ausente injustificado")
PRESENTE = 0; AUS_J = 1; AUS_I = 2

# Estados de alumno
ESTADOS_ALUMNO = ("Activo", "Inactivo")
AL_ACTIVO = 0; AL_INACTIVO = 1

# Estados de asistencia en CSV (códigos cortos)
ESTADOS_CSV = ("P", "AJ", "AI", "")  # "" = sin marcar
MAP_CSV_A_NOMBRE = {
    "P": ESTADOS_ASISTENCIA[PRESENTE],
    "AJ": ESTADOS_ASISTENCIA[AUS_J],
    "AI": ESTADOS_ASISTENCIA[AUS_I],
    "": "",
}
MAP_NOMBRE_A_CSV = {
    ESTADOS_ASISTENCIA[PRESENTE]: "P",
    ESTADOS_ASISTENCIA[AUS_J]: "AJ",
    ESTADOS_ASISTENCIA[AUS_I]: "AI",
    "": "",
}

# Encabezado de columnas del archivo CSV
CABECERA_CSV = ("clase_id", "legajo", "apellido", "nombre", "estado")
CSV_SEP = ";"

# Reglas del sistema
PORC_MAX_INASISTENCIA = 25.0   # baja lógica si AI% > 25
DECIMALES_PORCENTAJE = 2       # formato de porcentaje

# Rangos de IDs base
ID_DOCENTE_INICIAL = 10000
ID_CLASE_INICIAL = 20000
ID_ALUMNO_INICIAL = 30000