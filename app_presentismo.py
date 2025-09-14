# importar funciones y variables

from core import (
    # menús y validadores
    mostrar_menu_principal, mostrar_menu_alumnos, mostrar_menu_reportes,
    opcion_valida_menu,

    # datos de alumnos para listado rápido
    alumnos,clases,asistencias, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, AL_EMAIL, PRESENTE
)

# login
from login import login_usuario

from funcionalidades.alumnos import (
    alta_alumno, baja_alumno, modificar_dato_alumno,
)

from core.datos import (
    alumnos_baja
)

from funcionalidades.Reportes import (
    reporte_asistencia_por_estudiante,
    reporte_asistencia_general,
    reporte_por_clase
)
from funcionalidades.asistencia import(
    gestion_asistencias
)

def listar_alumnos():
    if not alumnos:
        print("Sin alumnos.")
        return
    print(f"{'LEGAJO':<8}| {'APELLIDO':<15} | {'NOMBRE':<14} | {'EMAIL':<27}")
    print("-" * 70)
    for a in alumnos:
       print(f"{a[AL_LEGAJO ]:<6} | {a[AL_APELLIDO]:<15} | {a[AL_NOMBRE]:<12} | {a[AL_EMAIL]:<27}")
    print() 


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
        elif opcion == "2":
            alta_alumno(alumnos, alumnos_baja)
            print("Alta de alumno.")
        elif opcion == "3":
            print("Baja lógica de alumno.")
            baja_alumno(alumnos, alumnos_baja)
        elif opcion == "4":
            print("Modificar alumno.")
            modificar_dato_alumno(alumnos)           
    return "volver"


# Asegúrate de tener las variables asistencias, estudiantes y clases disponibles.
# Ejemplo de menú de reportes adaptado:
def menu_reportes():
    en_reportes = True
    while en_reportes:
        mostrar_menu_reportes()
        opcion = input("Elegí una opción: ").strip()

        if not opcion_valida_menu(opcion, {"0", "1", "2", "3", "9"}):
            print("Opción inválida.")
        elif opcion == "0":
            en_reportes = False
        elif opcion == "9":
            return "logout"
        elif opcion == "1":
            print(reporte_asistencia_general(asistencias))
        elif opcion == "2":
            # Encabezado de la tabla
            print(f"{'LEGAJO':<8} {'APELLIDO':<15} {'NOMBRE':<14} {'PRESENTES':<10} {'TOTAL':<7} {'% ASISTENCIA':<13}")
            print("-" * 65)
            for alumno in alumnos:
                legajo = alumno[AL_LEGAJO]
                apellido = alumno[AL_APELLIDO]
                nombre = alumno[AL_NOMBRE]
                # Calcula presentes y total
                total = 0
                presentes = 0
                for (clase_id, l), estado in asistencias.items():
                    if l == legajo:
                        total += 1
                        if estado == PRESENTE:
                            presentes += 1
                porcentaje = (presentes / total) * 100 if total > 0 else 0
                print(f"{legajo:<8} {apellido:<15} {nombre:<14} {presentes:<10} {total:<7} {porcentaje:>10.2f}%")
            print()
        elif opcion == "3":
            for clase_id in clases:
                print(reporte_por_clase(asistencias, alumnos, clases, clase_id))
                print()
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