# Validadores básicos (sin try/except por ahora porque lo vemos en la clase 10)

# Menús (opciones) valida que la opción ingresada esté dentro de las opciones válidas

def opcion_valida_menu(opcion, validas):
    return opcion in validas

# Datos numéricos

# DNI válido: 7 u 8 dígitos numéricos

def dni_valido(dni):
    return dni.isdigit() and 7 <= len(dni) <= 8

# Legajo válido: entero positivo (string de dígitos > 0)

def legajo_valido(legajo):
    return legajo.isdigit() and int(legajo) > 0

# True si valor es string de dígitos y su entero es > 0

def entero_positivo_str(valor):
    return valor.isdigit() and int(valor) > 0

# True si valor es string de dígitos y el entero está entre [minimo, maximo].

def entero_en_rango_str(valor, minimo, maximo):
    if not valor.isdigit():
        return False
    n = int(valor)
    return minimo <= n <= maximo


# Textos (no vacíos, mínimos)

# True si el texto no está vacío al quitar espacios
def no_vacio(texto):
    return len(texto.strip()) > 0

# Nombre válido: mínimo 'min_len' caracteres no vacíos

def nombre_valido(nombre, min_len=2):
    return len(nombre.strip()) >= min_len

# Apellido válido: mínimo 'min_len' caracteres no vacíos
def apellido_valido(apellido, min_len=2):
    return len(apellido.strip()) >= min_len

# Validación de email: contiene '@', '.' y tiene largo mínimo razonable

def email_valido(email):
    e = email.strip()
    return "@" in e and "." in e and len(e) > 5

# Password válida: longitud mínima

def password_valida(password, min_len=4):
    return len(password) >= min_len

# Fechas formato dd-mm-aaaa

# Fecha válida simple en formato dd-mm-aaaa. Chequea: 3 partes separadas por '-', todas dígitos, rangos básicos de día/mes/año (No considera meses con 30/31 días ni bisiestos exactos

def fecha_ddmmyyyy_valida(fecha):
    partes = fecha.strip().split("-")
    if len(partes) != 3:
        return False

    d, m, y = partes[0], partes[1], partes[2]
    if not (d.isdigit() and m.isdigit() and y.isdigit()):
        return False

    d = int(d); m = int(m); y = int(y)
    if not (1 <= d <= 31 and 1 <= m <= 12 and 1900 <= y <= 2100):
        return False

    return True
