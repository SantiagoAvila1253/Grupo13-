# Validadores

# Menús con opciones

# Devuelve True si 'opcion' está dentro de 'validas'

def opcion_valida_menu(opcion, validas):
    return opcion in validas

def estado_asistencia_valido(valor, validos):
    return valor in validos

# Datos numéricos

# DNI válido si tiene 7 u 8 dígitos

def dni_valido(dni):
    return dni.isdigit() and 7 <= len(dni) <= 8

# Legajo válido si es string de dígitos y su entero > 0

def legajo_valido_str(valor):
    return valor.isdigit() and int(valor) > 0

# Compatibilidad con dato existente

def legajo_valido(legajo):
    return legajo_valido_str(legajo)

# True si es string de dígitos y > 0

def entero_positivo_str(valor):
    return valor.isdigit() and int(valor) > 0

# True si es string de dígitos y el entero está entre dos valores

def entero_en_rango_str(valor, minimo, maximo):
    if not valor.isdigit():
        return False
    n = int(valor)
    return minimo <= n <= maximo

# Textos

# True si el texto no está vacío

def no_vacio(texto):
    return len(texto.strip()) > 0

# True si tiene al menos 'min_len' caracteres no vacíos

def nombre_valido(nombre, min_len=2):
    return len(nombre.strip()) >= min_len

# True si tiene al menos 'min_len' caracteres no vacíos

def apellido_valido(apellido, min_len=2):
    return len(apellido.strip()) >= min_len

# Validación simple de email: contiene '@' y '.', y largo mínimo

def email_valido(email):
    e = email.strip()
    return "@" in e and "." in e and len(e) > 5

# Contraseñas 

# True si cumple requisito de cantidad de caracteres

def password_valida(password, min_len=4):
    return len(password) >= min_len


# Fechas (dd-mm-aaaa) - validación simple

"""
- 3 partes separadas por '-'
- todas dígitos
- rangos básicos: 1<=d<=31, 1<=m<=12, 1915<=a<=2009
(No valida meses de 30/31 ni años bisiestos exactos.)
"""

def fecha_ddmmyyyy_valida(fecha):
    partes = fecha.strip().split("-")
    if len(partes) != 3:
        return False

    d, m, a = partes[0], partes[1], partes[2]
    if not (d.isdigit() and m.isdigit() and a.isdigit()):
        return False

    d = int(d); m = int(m); a = int(a)
    if not (1 <= d <= 31 and 1 <= m <= 12 and 1915 <= a <= 2009):
        return False

    return True
