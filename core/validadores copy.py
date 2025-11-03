# Importar expresiones regulares
import re

# Patrones precompilados

# Permite ceros a la izquierda, pero exige valor > 0 (rechaza "0", "0000", etc.)
RE_LEGAJO = re.compile(r'^0*[1-9]\d*$')

# DNI: exactamente 7 u 8 dígitos
RE_DNI = re.compile(r'^\d{7,8}$')

# Email: parte local con ._%+-, dominio con . y -, y TLD de 2+ letras
RE_EMAIL = re.compile(r'^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$')

# Estados válidos: '0' (Presente), '1' (AJ), '2' (AI)
RE_ESTADO = re.compile(r'^[012]$')

# Fecha: dd-mm-aaaa o dd/mm/aaaa (formato correcto)
RE_FECHA_FMT = re.compile(
    r'^(0[1-9]|[12]\d|3[01])[-/](0[1-9]|1[0-2])[-/](19\d{2}|20\d{2})$'
)

# Nombres/Apellidos: letras (incluye acentos/ñ), espacios, ' y -, mínimo 2 chars
RE_NOM_AP = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]{2,}$")

# Funciones

#  Menús / opciones
def opcion_valida_menu(opcion, validas):
    return opcion in validas

# Valida formato (regex 0|1|2) y exige pertenencia al set 'validos'
def estado_asistencia_valido(valor, validos):
    v = valor.strip()
    return bool(RE_ESTADO.fullmatch(v)) and v in validos

# Numéricos

# DNI True si DNI tiene 7 u 8 dígitos
def dni_valido(dni):
    return bool(RE_DNI.fullmatch(dni.strip()))

#  Texto

# Nombre y apellido
def nom_ape_valido(nombre, min_len=2):
    s = nombre.strip()
    return bool(RE_NOM_AP.fullmatch(s))

# Email completo; '\.' asegura punto literal
def email_valido(email):
    return bool(RE_EMAIL.fullmatch(email.strip()))

# Contraseña Regla mínima de longitud
def password_valida(password, min_len=4):
    return len(password) >= min_len

#  Fechas

# True si el año 'a' es bisiesto
def es_bisiesto(a):
    return (a % 4 == 0 and a % 100 != 0) or (a % 400 == 0)

""" Acepta dd-mm-aaaa o dd/mm/aaaa. Valida formato completo con regex; chequea días según mes y febrero bisiesto.
    Rango de año 1915-2009"""
def fecha_ddmmaaaa_valida(fecha):
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

