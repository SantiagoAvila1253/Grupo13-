# importar menú, validadores y funciones

from core import (mostrar_menu_principal, opcion_valida_menu)
from login import login_usuario
from funcionalidades import (menu_alumnos, menu_reportes, gestion_asistencias)

# controla la sesión logueada
# - 'logout' si el usuario cierra sesión,
# - 'exit' si elige Salir del sistema,
# - 'volver' si vuelve al menú anterior
def ciclo_sesion():
    en_sistema = True
    while en_sistema:
        mostrar_menu_principal()
        opcion = input("Elegí una opción: ").strip()
        if not opcion_valida_menu(opcion, {"0", "1", "2", "3", "9"}):
            print("Opción inválida.")
        elif opcion == "0":
            print("Fin.")
            return "exit"
        elif opcion == "9":
            # cerrar sesión desde el principal
            return "logout"
        elif opcion == "1":
            r = menu_alumnos()
            if r == "logout":
                return "logout"
        elif opcion == "2":
            # Gestión de asistencias: entrar directo al panel del módulo
            r = gestion_asistencias()
            if r == "logout":
                return "logout"
            # si vuelve de la gestión, seguimos en el menú principal
        elif opcion == "3":
            r = menu_reportes()
            if r == "logout":
                return "logout"
    return "volver"

# aplicación principal
def main():
    # permite re-loguear tras 'Cerrar sesión'
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

if __name__ == "__main__":
    main()