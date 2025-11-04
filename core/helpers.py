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
    Solicita una contraseña de forma segura, mostrando asteriscos (*) en Windows o
    sin mostrar caracteres en otros sistemas operativos.

    Comportamiento detallado:
    --------------------------
    - La función detecta el sistema operativo usando `sys.platform`.
      Si es Windows, utiliza el módulo `msvcrt` para capturar las teclas una por una
      sin que se impriman en la consola. En otros sistemas usa `getpass.getpass()`.

    - Mientras el usuario escribe:
        * Cada carácter válido se guarda internamente en la variable `password`.
          En pantalla solo se imprime un asterisco (*) para ocultar su valor real.
        * La tecla Backspace (código ASCII `\\x08`) elimina el último carácter
          tanto en la variable como visualmente (borrando un asterisco).
        * La tecla Enter (códigos `\\r` o `\\n`) finaliza el ingreso.
        * La tecla Escape (código `\\x1b`) cancela la operación y devuelve "".

    - `flush=True` fuerza que los asteriscos o los borrados se vean inmediatamente,
      sin esperar a que la consola vacíe su buffer.

    - Al finalizar, la función devuelve el texto REAL ingresado por el usuario
      (sin los asteriscos), que puede luego compararse con una contraseña guardada.

    Ejemplo:
    --------
    Usuario escribe: M, a, r, i, a, Backspace, Enter

        Pantalla muestra: *****
        Valor real devuelto: "Mari"

    Seguridad:
    ----------
    - En ningún momento se imprime la contraseña real.
    - No se almacenan logs ni copias temporales visibles.
    - Es compatible con Windows, Linux y macOS.
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
