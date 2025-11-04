# Funciones de ayuda integradas

from core import validadores as val
from core.es_json import leer_alumnos, leer_clases


# Valida legajo existente
def pedir_legajo_existente(etiqueta="Legajo"):
    """
    Pide un legajo por input hasta que:
        - sea entero positivo
        - exista como clave en data/alumnos.json
    Devuelve el legajo como int.
    """
    alumnos = leer_alumnos()  # diccionario de diccionarios
    while True:
        texto = input(f"{etiqueta}: ").strip()
        if not val.validar_numero_entero(texto):
            print(f"{etiqueta} inválido: debe ser un entero.")
            continue
        if not val.validar_legajo_formato(texto):
            print(f"{etiqueta} inválido: debe ser mayor que 0.")
            continue
        if not val.validar_legajo_existente(texto, alumnos):
            print(f"{etiqueta} inexistente: {texto}")
            continue
        return int(texto)


# Valida clase existente
def pedir_id_clase_existente(etiqueta="ID de clase"):
    """
    Pide un id de clase por input hasta que:
        - sea entero positivo
        - exista como clave en data/clases.json
    Devuelve el id de clase como int.
    """
    clases = leer_clases()
    while True:
        texto = input(f"{etiqueta}: ").strip()
        if not val.validar_numero_entero(texto):
            print(f"{etiqueta} inválido: debe ser un entero.")
            continue
        if not val.validar_id_clase_formato(texto):
            print(f"{etiqueta} inválido: debe ser mayor que 0.")
            continue
        if not val.validar_id_clase_existente(texto, clases):
            print(f"{etiqueta} inexistente: {texto}")
            continue
        return int(texto)
    

# Entrada segura de contraseña (multiplataforma)
def pedir_password(prompt="Contraseña: "):
    """
    Pide una contraseña de forma segura:
    - En Windows: muestra asteriscos (*) al escribir.
    - En Linux / Mac: oculta los caracteres con getpass.
    """
    import sys

    # Detección del sistema operativo
    if sys.platform.startswith("win"):
        import msvcrt
        print(prompt, end="", flush=True)
        password = ""

        while True:
            tecla = msvcrt.getch()
            # Caso base: Enter fin de ingreso
            if tecla in (b"\r", b"\n"):
                print()
                break
            # Backspace borrar un carácter
            elif tecla == b"\x08":
                if len(password) > 0:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            # ESC cancelar ingreso
            elif tecla == b"\x1b":
                print("\nCancelado.")
                return ""
            # Caso recursivo reducido (nuevo carácter)
            else:
                try:
                    char = tecla.decode("utf-8")
                except UnicodeDecodeError:
                    continue
                password += char
                print("*", end="", flush=True)

        return password

    else:
        # En otros sistemas usa getpass (sin mostrar caracteres)
        import getpass
        return getpass.getpass(prompt)
