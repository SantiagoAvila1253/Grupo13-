from core import (
    mostrar_menu_principal, mostrar_menu_alumnos, mostrar_menu_asistencia, mostrar_menu_reportes,
    opcion_valida_menu, alumnos, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, AL_EMAIL
)
from login import login_usuario


def listar_alumnos():
    if not alumnos:
        print("Sin alumnos.")
        return
    print("\nLEGAJO | APELLIDO, NOMBRE | EMAIL")
    for a in alumnos:
        print(f"{a[AL_LEGAJO]} | {a[AL_APELLIDO]}, {a[AL_NOMBRE]} | {a[AL_EMAIL]}")


def menu_alumnos():
    en_alumnos = True
    while en_alumnos:
        mostrar_menu_alumnos()
        aop = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(aop, {"0", "1", "2", "3", "4", "9"}):
            print("Opción inválida.")
        elif aop == "0":
            en_alumnos = False
        elif aop == "9":
            return "logout"
        elif aop == "1":
            listar_alumnos()
        elif aop == "2":
            print("Alta de alumno (pendiente).")
        elif aop == "3":
            print("Baja lógica de alumno (pendiente).")
        elif aop == "4":
            print("Modificar alumno (pendiente).")
    return "volver"


def menu_asistencia():
    en_asistencia = True
    while en_asistencia:
        mostrar_menu_asistencia()
        sop = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(sop, {"0", "1", "2", "9"}):
            print("Opción inválida.")
        elif sop == "0":
            en_asistencia = False
        elif sop == "9":
            return "logout"
        elif sop == "1":
            print("Registrar asistencia (pendiente).")
        elif sop == "2":
            print("Consultar asistencia por fecha (pendiente).")
    return "volver"


def menu_reportes():
    en_reportes = True
    while en_reportes:
        mostrar_menu_reportes()
        rop = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(rop, {"0", "1", "2", "9"}):
            print("Opción inválida.")
        elif rop == "0":
            en_reportes = False
        elif rop == "9":
            return "logout"
        elif rop == "1":
            print("Presentes por clase (pendiente).")
        elif rop == "2":
            print("Porcentaje de asistencia por alumno (pendiente).")
    return "volver"


"""Controla la sesión logueada:
    - 'logout' si el usuario cierra sesión,
    - 'exit' si elige Salir del sistema,
    - 'volver' en caso que el usuario quiera volver al menú anterior
    """
def ciclo_sesion():
    en_sistema = True
    while en_sistema:
        mostrar_menu_principal()
        op = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(op, {"0", "1", "2", "3", "9"}):
            print("Opción inválida.")
        elif op == "0":
            print("Fin.")
            return "exit"
        elif op == "9":
            # Cerrar sesión desde el principal
            return "logout"
        elif op == "1":
            r = menu_alumnos()
            if r == "logout":
                return "logout"
        elif op == "2":
            r = menu_asistencia()
            if r == "logout":
                return "logout"
        elif op == "3":
            r = menu_reportes()
            if r == "logout":
                return "logout"
    return "volver"


def main():
    # Loop de aplicación completo, permitiendo re-loguear tras 'Cerrar sesión'
    ejecutando = True
    while ejecutando:
        usuario = login_usuario()
        if not usuario:
            print("Saliste del sistema.")
            return

        resultado = ciclo_sesion()
        if resultado == "exit":
            ejecutando = False
        elif resultado == "logout":
            print("Cerraste tu sesión.")
            # sigue el while y vuelve a pedir login


if __name__ == "__main__":
    main()
