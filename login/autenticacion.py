# Módulo autenticacion
"""
Responsabilidades:
- Gestionar el login de usuarios (docentes).
- Validar credenciales usando los datos del JSON de docentes.
- Permitir el reseteo seguro de contraseñas (ingreso protegido).
"""

from core import menus, validadores, es_json
from core.helpers import pedir_password
from core.es_json import pausa

from colorama import Fore, Style

# Auxiliar: validación recursiva de credenciales
def validar_credenciales_rec(dic_docentes, dni, clave, claves, i=0):
    """
    Busca recursivamente un docente válido por DNI y clave.
    - Caso base: si se recorrieron todas las claves → False.
    - Reducción de dominio: avanza al siguiente índice.
    """
    if i == len(claves):
        return False  # caso base

    clave_actual = claves[i]
    datos = dic_docentes[clave_actual]

    if str(datos.get("dni")) == str(dni) and str(datos.get("clave")) == str(clave):
        return True

    # caso recursivo + reducción del dominio
    return validar_credenciales_rec(dic_docentes, dni, clave, claves, i + 1)


# Auxiliar: actualización recursiva de contraseña
def actualizar_clave_rec(dic_docentes, dni, nueva_clave, claves, i=0):
    """
    Actualiza la contraseña de un docente de forma recursiva.
    - Caso base: si se recorrieron todas las claves → False.
    - Reducción de dominio: avanza al siguiente índice.
    """
    if i == len(claves):
        return False  # caso base

    clave_actual = claves[i]
    datos = dic_docentes[clave_actual]

    if str(datos.get("dni")) == str(dni):
        datos["clave"] = str(nueva_clave)
        return True

    # caso recursivo + reducción del dominio
    return actualizar_clave_rec(dic_docentes, dni, nueva_clave, claves, i + 1)


# Resetear clave
def reiniciar_clave():
    """
    Permite reiniciar la contraseña de un docente existente.
    - Ingreso protegido con pedir_password (Windows: '*' / otros OS: oculto).
    - Pide confirmación de la nueva contraseña.
    """
    try:
        docentes = es_json.leer_docentes()
        dni = input(Fore.YELLOW + "Ingresá tu DNI: " + Style.RESET_ALL).strip()

        if not validadores.dni_valido(dni):
            print(Fore.RED + "DNI inválido.")
            pausa()
            return False

        nueva = pedir_password("Nueva contraseña (mínimo 4 caracteres): ")
        if not validadores.password_valida(nueva, 4):
            print(Fore.RED + "Contraseña inválida (mínimo 4 caracteres).")
            pausa()
            return False

        confirma = pedir_password("Repetí la nueva contraseña: ")
        if nueva != confirma:
            print(Fore.RED + "Las contraseñas no coinciden.")
            pausa()
            return False

        # Actualización (recursiva) y persistencia
        if actualizar_clave_rec(docentes, dni, nueva, list(docentes.keys())):
            es_json.guardar_json("data/docentes.json", docentes)
            print(Fore.GREEN + "Contraseña actualizada.")
            pausa()
            return True

        print(Fore.RED + "Usuario no encontrado.")
        pausa()
        return False

    except Exception as error:
        print(Fore.RED + f"No se pudo reiniciar la clave. Tipo de error: {type(error).__name__}. Detalle: {error}")
        pausa()
        return False


# Login de usuario (controlador del ciclo)
def login_usuario():
    """
    Controla el flujo del login (menú + validaciones).
    Implementación recursiva de flujo:
      - Caso base: salir o login correcto → retorna dict/None.
      - Caso recursivo: opción inválida / DNI inválido / credenciales incorrectas → reintenta.
      - Reducción del dominio: cada intento vuelve a pedir solo el dato necesario.
    """
    try:
        menus.mostrar_menu_login()
        opcion = input(Fore.YELLOW + "\nElegí una opción: " + Style.RESET_ALL).strip()

        # Validación de opción
        if not validadores.opcion_valida_menu(opcion, {"1", "2", "3"}):
            print(Fore.RED + "Opción inválida.")
            pausa()
            return login_usuario()  # caso recursivo

        # Opción 1: iniciar sesión
        if opcion == "1":
            docentes = es_json.leer_docentes()
            dni = input(Fore.YELLOW + "\nIngresá tu DNI (sin puntos ni comas o -1 para salir): " + Style.RESET_ALL).strip()
            if dni == "-1":
                return None  # caso base

            if not validadores.dni_valido(dni):
                print(Fore.RED + "DNI inválido.")
                pausa()
                return login_usuario()  # recursivo

            clave = pedir_password("Ingresá tu contraseña: ")

            ok = validar_credenciales_rec(docentes, dni, clave, list(docentes.keys()))
            if ok:
                print(Fore.GREEN + "Login correcto.")
                pausa()
                return {"dni": dni}  # caso base
            else:
                print(Fore.RED + "Credenciales incorrectas.")
                pausa()
                return login_usuario()  # recursivo

        # Opción 2: resetear clave
        if opcion == "2":
            reiniciar_clave()
            return login_usuario()  # recursivo (volver al menú de login)

        # Opción 3: salir
        if opcion == "3":
            return None  # caso base

    except Exception as error:
        print(Fore.RED + f"No se pudo ejecutar el login. Tipo de error: {type(error).__name__}. Detalle: {error}")
        pausa()
        return None