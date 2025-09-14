# Validadores

# Menús con opciones

# Devuelve True si 'opcion' está dentro de 'validas'

def opcion_valida_menu(opcion, validas):
    validar = opcion in validas
    return validar

def estado_asistencia_valido(valor, validos):
    validar = valor in validos
    return validar

# Datos numéricos

# DNI válido si tiene 7 u 8 dígitos

def dni_valido(dni):
    validar = dni.isdigit() and 7 <= len(dni) <= 8
    return validar

# Legajo válido si es string de dígitos y su entero > 0

def legajo_valido_str(valor):
    validar = valor.isdigit() and int(valor) > 0
    return validar

# Compatibilidad con dato existente

def legajo_valido(legajo):
    validar = legajo_valido_str(legajo)
    return validar

# True si es string de dígitos y > 0

def entero_positivo_str(valor):
    validar = valor.isdigit() and int(valor) > 0
    return validar

# True si es string de dígitos y el entero está entre dos valores

def entero_en_rango_str(valor, minimo, maximo):
    if not valor.isdigit():
        return False
    n = int(valor)
    validar = minimo <= n <= maximo
    return validar

# Textos

# True si el texto no está vacío

def no_vacio(texto):
    validar = len(texto.strip()) > 0
    return validar

# True si tiene al menos 'min_len' caracteres no vacíos

def nombre_valido(nombre, min_len=2):
    validar = len(nombre.strip()) >= min_len
    return validar

# True si tiene al menos 'min_len' caracteres no vacíos

def apellido_valido(apellido, min_len=2):
    validar = len(apellido.strip()) >= min_len
    return validar

# Validación simple de email: contiene '@' y '.', y largo mínimo

def email_valido(email):
    e = email.strip()
    validar = "@" in e and "." in e and len(e) > 5
    return validar

# Contraseñas 

# True si cumple requisito de cantidad de caracteres

def password_valida(password, min_len=4):
    validar = len(password) >= min_len
    return validar

# Validar bisiesto
"""
True si 'a' (año) es bisiesto:
- divisible por 4 y no por 100, o
- divisible por 400
"""

def es_bisiesto(a):
    validar = (a % 4 == 0 and a % 100 != 0) or (a % 400 == 0)
    return validar

# Valida formato fecha con 'dd-mm-aaaa'

"""
- 3 partes separadas por '-'
- todas dígitos
- rangos exactos por mes (30/31) y febrero con bisiestos
- rango de año acotado
"""

def fecha_ddmmaaaa_valida(fecha):
    partes = fecha.strip().split("-")
    if len(partes) != 3:
        return False

    d, m, a = partes[0], partes[1], partes[2]
    if not (d.isdigit() and m.isdigit() and a.isdigit()):
        return False

    d = int(d); m = int(m); a = int(a)

    # Rango de año según edades posibles estimadas
    if not (1915 <= a <= 2009):
        return False

    if not (1 <= m <= 12):
        return False

    # Días por mes con febrero bisiesto
    if m in (1, 3, 5, 7, 8, 10, 12):
        max_dias = 31
    elif m in (4, 6, 9, 11):
        max_dias = 30
    else:
        max_dias = 29 if es_bisiesto(a) else 28
    validar = 1 <= d <= max_dias
    return validar
