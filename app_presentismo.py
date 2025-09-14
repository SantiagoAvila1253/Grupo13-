# importar funciones y variables

from core import (
    # menús y validadores
    mostrar_menu_principal, mostrar_menu_alumnos, mostrar_menu_reportes,
    opcion_valida_menu,

    # datos de alumnos para listado rápido
    alumnos, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, AL_EMAIL,
)

# login
from login import login_usuario

from funcionalidades.alumnos import (
    alta_alumno, baja_alumno, modificar_dato_alumno,
)

from core.datos import (
    alumnos_baja
)

def listar_alumnos():
    if not alumnos:
        print("Sin alumnos.")
        return
    print("\nLEGAJO | APELLIDO, NOMBRE | EMAIL")
    for a in alumnos:
        if len(a) > max(AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, AL_EMAIL):
            print(f"{a[AL_LEGAJO]} | {a[AL_APELLIDO]}, {a[AL_NOMBRE]} | {a[AL_EMAIL]}")
        else:
            print("Alumno mal cargado:", a)


# menú alumnos
def menu_alumnos():
    en_alumnos = True
    while en_alumnos:
        mostrar_menu_alumnos()
        opcion = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(opcion, {"0", "1", "2", "3", "4", "9"}):
            print("Opción inválida.")
        elif opcion == "0":
            en_alumnos = False
        elif opcion == "9":
            return "logout"
        elif opcion == "1":
            listar_alumnos()
        elif aop == "2":
            alta_alumno(alumnos, alumnos_baja)
            print("Alta de alumno.")
        elif aop == "3":
            print("Baja lógica de alumno.")
            baja_alumno(alumnos, alumnos_baja)
        elif aop == "4":
            print("Modificar alumno.")
            modificar_dato_alumno(alumnos)           
    return "volver"


# menú reportes (placeholder)
def menu_reportes():
    en_reportes = True
    while en_reportes:
        mostrar_menu_reportes()
        opcion = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(opcion, {"0", "1", "2", "9"}):
            print("Opción inválida.")
        elif opcion == "0":
            en_reportes = False
        elif opcion == "9":
            return "logout"
        elif opcion == "1":
            print("Presentes por clase (pendiente).")
        elif opcion == "2":
            print("Porcentaje de asistencia por alumno (pendiente).")
    return "volver"


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