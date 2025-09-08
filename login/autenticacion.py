# importar funciones y variables

from core import (
    mostrar_menu_login, opcion_valida_menu,
    dni_valido, password_valida,
    DOCENTES, DO_DNI, DO_CLAVE
)

# login

def login_usuario():
    while True:
        mostrar_menu_login()
        op = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(op, {"1", "2", "3"}):
            print("Opción inválida.")
        elif op == "1":
            dni = input("Ingresá tu DNI sin puntos ni comas o -1 para salir): ").strip()
            if dni == "-1":
                return None
            if not dni_valido(dni):
                print("DNI inválido.")
            else:
                clave = input("Ingresá tu Contraseña: ")
                ok = False
                for item in DOCENTES:
                    if item[DO_DNI] == dni and item[DO_CLAVE] == clave:
                        ok = True
                if ok:
                    print("Login correcto.")
                    return {"dni": dni}
                else:
                    print("Contraseña incorrecta. Probá  de nuevo o reseteá tu contraseña.")
        elif op == "2":
            reiniciar_clave()
        elif op == "3":
            return None


def reiniciar_clave():
    dni = input("Ingresá tu DNI: ").strip()
    if not dni_valido(dni):
        print("DNI inválido.")
        return False

    nueva = input("Nueva contraseña (mínimo 4 caracteres): ")
    if not password_valida(nueva, 4):
        print("Inválida.")
        return False

    for item in DOCENTES:
        if item[DO_DNI] == dni:
            item[DO_CLAVE] = nueva
            print("Contraseña actualizada.")
            return True

    print("Usuario no encontrado.")
    return False
