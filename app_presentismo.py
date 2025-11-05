# Control de sesión y ruteo de menús

# Imports
from core import (mostrar_menu_principal, opcion_valida_menu)
from login import login_usuario
from funcionalidades import (menu_alumnos, menu_reportes, gestion_asistencias, menu_filtros)


# control de la sesión
def ciclo_sesion():
    """
      - 'logout' si el usuario cierra sesión,
      - 'exit' si elige Salir del sistema,
      - 'volver' si vuelve al menú anterior.
    """
    en_sistema = True
    while en_sistema:
        mostrar_menu_principal()
        opcion = input("Elegí una opción: ").strip()

        # Menú principal actualizado: 1=Alumnos, 2=Asistencias, 3=Filtros, 4=Reportes, 9=Cerrar sesión, 0=Salir
        if not opcion_valida_menu(opcion, {"0", "1", "2", "3", "4", "9"}):
            print("Opción inválida.")
            continue

        if opcion == "0":
            print("Fin.")
            return "exit"

        if opcion == "9":
            return "logout"

        if opcion == "1":
            r = menu_alumnos()
            if r == "logout":
                return "logout"
            # si vuelve, continúa en el principal
            continue

        if opcion == "2":
            r = gestion_asistencias()
            if r == "logout":
                return "logout"
            continue

        if opcion == "3":
            r = menu_filtros()
            if r == "logout":
                return "logout"
            continue

        if opcion == "4":
            r = menu_reportes()
            if r == "logout":
                return "logout"
            continue

    return "volver"


# Aplicación principal
def main():
    """
      - login
      - ciclo de sesión (con posibilidad de re-logueo tras 'Cerrar sesión')
    """
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


# Iniciar main
if __name__ == "__main__":
    main()