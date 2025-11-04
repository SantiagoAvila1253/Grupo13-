# core/validadores.py

import re
from datetime import datetime

# Patrones precompilados (regex)

# Legajo/ID: permite ceros a la izquierda, pero exige valor > 0 (rechaza "0", "0000", etc.)
RE_LEGAJO = re.compile(r'^0*[1-9]\d*$')

# DNI: exactamente 7 u 8 dígitos
RE_DNI = re.compile(r'^\d{7,8}$')

# Email: parte local con ._%+-, dominio con . y -, y TLD de 2+ letras
RE_EMAIL = re.compile(r'^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$')

# Fecha dd-mm-aaaa o dd/mm/aaaa (formato correcto, no rango semántico)
RE_FECHA_FMT = re.compile(
    r'^(0[1-9]|[12]\d|3[01])[-/](0[1-9]|1[0-2])[-/](19\d{2}|20\d{2})$'
)

# Nombres/Apellidos: letras (incluye acentos/ñ), espacios, ' y -, mínimo 2 chars
RE_NOM_AP = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]{2,}$")

# Estados de asistencia en CSV
ESTADOS_ASISTENCIA_VALIDOS = {"P", "AJ", "AI"}

# Validadores generales

# valida una opción de Sí/No
def validar_opcion_sn(valor):
    if not isinstance(valor, str):
        return False
    return valor.strip().lower() in {"s", "n"}


# valida que el texto sea una cadena no vacía
def validar_texto_no_vacio(texto):
    if not isinstance(texto, str):
        return False
    return texto.strip() != ""


# verifica si un valor puede convertirse a entero sin error
def validar_numero_entero(valor):
    try:
        int(valor)
        return True
    except Exception:
        return False


# verifica si un número es entero positivo (> 0)
def validar_numero_positivo(valor):
    try:
        return int(valor) > 0
    except Exception:
        return False


# Validadores específicos


# valida si una opción está dentro del conjunto/lista 'validas'
def opcion_valida_menu(opcion, validas):
    return opcion in validas


# DNI válido si tiene 7 u 8 dígitos
def dni_valido(dni):
    if not isinstance(dni, str):
        return False
    return bool(RE_DNI.fullmatch(dni.strip()))


# valida nombre/apellido: letras (incluye acentos/ñ), espacios, ' y -, mínimo 2 caracteres
def nom_ape_valido(nombre, min_len=2):
    if not isinstance(nombre, str):
        return False
    s = nombre.strip()
    if len(s) < min_len:
        return False
    return bool(RE_NOM_AP.fullmatch(s))


# Email válido (formato general)
def email_valido(email):
    if not isinstance(email, str):
        return False
    return bool(RE_EMAIL.fullmatch(email.strip()))


# Contraseña: regla mínima de longitud
def password_valida(password, min_len=4):
    if not isinstance(password, str):
        return False
    return len(password) >= min_len


# True si el año es bisiesto.
def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)


# Acepta dd-mm-aaaa o dd/mm/aaaa - Valida formato y días según mes y febrero bisiesto
def fecha_ddmmaaaa_valida(fecha):
    if not isinstance(fecha, str):
        return False

    s = fecha.strip()
    if len(s) != 10:
        return False
    if s[2] not in "-/" or s[5] not in "-/":
        return False

    dia_str = s[0:2]
    mes_str = s[3:5]
    anio_str = s[6:10]

    if not (dia_str.isdigit() and mes_str.isdigit() and anio_str.isdigit()):
        return False

    dia = int(dia_str)
    mes = int(mes_str)
    anio = int(anio_str)

    if not (1915 <= anio <= 2009):
        return False
    if not (1 <= mes <= 12):
        return False

    if mes in (1, 3, 5, 7, 8, 10, 12):
        max_dias = 31
    elif mes in (4, 6, 9, 11):
        max_dias = 30
    else:
        max_dias = 29 if es_bisiesto(anio) else 28

    return 1 <= dia <= max_dias


# verifica que el legajo cumpla el patrón (> 0, permite ceros a la izquierda)
def validar_legajo_formato(legajo):
    if legajo is None:
        return False
    return bool(RE_LEGAJO.fullmatch(str(legajo)))


# verifica que el ID de clase sea entero positivo (> 0)
def validar_id_clase_formato(id_clase):
    return validar_numero_positivo(id_clase)


# valida que el legajo exista como clave en el diccionario de alumnos (claves string)
def validar_legajo_existente(legajo, alumnos_json):
    if not validar_legajo_formato(legajo):
        return False
    return str(int(legajo)) in alumnos_json


# valida que el id de clase exista como clave en el diccionario de clases (claves string)
def validar_id_clase_existente(id_clase, clases_json):
    if not validar_id_clase_formato(id_clase):
        return False
    return str(int(id_clase)) in clases_json


# Asistencia (CSV)


# Valida estado de asistencia (P, AJ, AI)
def validar_estado_asistencia(estado):
    if not isinstance(estado, str):
        return False
    return estado.strip().upper() in ESTADOS_ASISTENCIA_VALIDOS


# Verifica que una fila de asistencia tenga exactamente 5 columnas [clase_id, legajo, apellido, nombre, estado]
def validar_fila_csv(fila):
    if not isinstance(fila, (list, tuple)):
        return False
    return len(fila) == 5
