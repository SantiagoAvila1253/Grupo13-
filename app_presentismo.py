from core import (
    mostrar_menu_principal, mostrar_menu_alumnos, mostrar_menu_asistencia,
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

        if not opcion_valida_menu(aop, {"0", "1", "2", "3", "4"}):
            print("Opción inválida.")
        elif aop == "0":
            en_alumnos = False
        elif aop == "1":
            listar_alumnos()
        elif aop == "2":
            print("Alta de alumno (pendiente).")
        elif aop == "3":
            print("Baja lógica de alumno (pendiente).")
        elif aop == "4":
            print("Modificar alumno (pendiente).")


def main():
    usuario = login_usuario()
    if not usuario:
        print("Salida del sistema.")
        return

    en_sistema = True
    while en_sistema:
        mostrar_menu_principal()
        op = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(op, {"0", "1", "2", "3"}):
            print("Opción inválida.")
        elif op == "0":
            print("Fin.")
            en_sistema = False
        elif op == "1":
            menu_alumnos()
        elif op == "2":
            mostrar_menu_asistencia()
            sop = input("Elegí una opción: ").strip()
            if not opcion_valida_menu(sop, {"0", "1", "2"}):
                print("Opción inválida.")
            else:
                if sop == "0":
                    print("Volver.")
                elif sop == "1":
                    print("Registrar asistencia (pendiente).")
                elif sop == "2":
                    print("Consultar asistencia por fecha (pendiente).")
        elif op == "3":
            print("Reportes (pendiente).")


if __name__ == "__main__":
    main()
