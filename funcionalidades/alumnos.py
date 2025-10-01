# Módulo de ABM de alumnos:
# - Alta (nuevo / reactivar)
# - Baja lógica
# - Modificación de datos
# - Listado y menú de alumnos
# Integra validaciones (regex) y normaliza entradas antes de operar.

from core import (
    # Datos
    alumnos, alumnos_baja, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, AL_EMAIL,
    # Menú
    mostrar_menu_alumnos,
    # Validadores
    nom_ape_valido, fecha_ddmmaaaa_valida, email_valido, opcion_valida_menu,
    # Helpers
    legajo_valido
)

# Dar de alta un alumno (nuevo o reactivación)
def alta_alumno(alumnos, alumnos_baja):
    print("Alta de alumno ")
    print("1) Dar de alta a un alumno nuevo")
    print("2) Reactivar a un alumno existente")
    opcion = input("Ingresá una opcion: ").strip()

    # Reactivar un alumno dado de baja previamente
    if opcion == "2":
        if alumnos_baja:
            # Mostrar alumnos inactivos disponibles para reactivar
            print("Alumnos inactivos disponibles para reactivar:")
            print(f"{'ID':<5} | {'Nombre':<12} | {'Apellido':<15} | {'Email':<27}")
            print("-" * 75)
            for alumno in alumnos_baja:
                print(f"{alumno[0]:<5} | {alumno[3]:<12} | {alumno[2]:<15} | {alumno[5]:<27}")
            # Pedir y validar legajo
            id_reactivar = legajo_valido(tipo="inactivo")
            reactivar_alumno(id_reactivar, alumnos, alumnos_baja)
        else:
            print("No hay alumnos inactivos para reactivar.")
        return  # Termina la rama de reactivación

    # Dar de alta un alumno nuevo
    elif opcion == "1":
        # Nombre (solo letras, espacios, apóstrofo y guion; min 2)
        nombre = input("Nombre: ")
        while not nom_ape_valido(nombre):
            print("El nombre solo puede tener letras y al menos dos caracteres. Intentá de nuevo.")
            nombre = input("Nombre: ")

        # Apellido (mismo criterio que nombre)
        apellido = input("Apellido: ")
        while not nom_ape_valido(apellido):
            print("El apellido solo puede tener letras y al menos dos caracteres. Intentá de nuevo")
            apellido = input("Apellido: ")

        # Fecha de nacimiento (dd-mm-aaaa)
        fecha_nac = input("Fecha de nacimiento (dd-mm-aaaa): ")
        while not fecha_ddmmaaaa_valida(fecha_nac):
            print("Fecha inválida. Intente de nuevo.")
            fecha_nac = input("Fecha de nacimiento (dd-mm-aaaa): ")

        # Email
        email = input("Email: ")
        while not email_valido(email):
            print("Email inválido. Intente de nuevo.")
            email = input("Email: ")

        # Generar nuevo ID: base 1001 + cantidad en activos + cantidad en inactivos
        nuevo_id = 1001 + len(alumnos) + len(alumnos_baja)

        # Estructura del alumno: [ID, <campo reservado>, APELLIDO, NOMBRE, FECHA_NAC, EMAIL, ESTADO]
        alumnos.append([nuevo_id, " ", apellido, nombre, fecha_nac, email, 0])
        print(f" Alumno {nombre} {apellido} agregado correctamente con ID {nuevo_id}.")
        return

    else:
        print("Opcion no valida. Por favor, intente de nuevo.")
        return

# Dar de baja (lógica) un alumno
def baja_alumno(alumnos, alumnos_baja):
    print("Baja de alumno")
    # Pedir y validar legajo
    id_alumno = legajo_valido(tipo="alumno")

    # Mover de activos a inactivos si existe
    for alumno in alumnos:
        if alumno[0] == id_alumno:
            alumnos_baja.append(alumno)
            alumnos.remove(alumno)
            print(f" Alumno {alumno[3]} {alumno[2]} y ID {id_alumno} eliminado correctamente.")
            return
    print(" No se encontró un alumno con ese ID.")
    return

# Reactivar un alumno previamente dado de baja
def reactivar_alumno(id_reactivar, alumnos, alumnos_baja):
    # Buscar por ID en la lista de inactivos
    alumno_a_reactivar = list(filter(lambda x: x[0] == id_reactivar, alumnos_baja))
    if alumno_a_reactivar:
        alumnos.append(alumno_a_reactivar[0])
        alumnos_baja.remove(alumno_a_reactivar[0])
        # Mantener un criterio de orden (se respeta el campo existente índice 1)
        alumnos.sort(key=lambda x: x[1])
        print(f"El alumno con Id {id_reactivar} ha sido reactivado")
        return
    else:
        print(f" No se encontró un alumno con el ID {id_reactivar} en la lista de inactivos.")
        return

# Modificar datos de un alumno
def modificar_dato_alumno(alumnos):
    print("Modificar datos de un alumno")
    # Pedir y validar legajo
    id_alumno = legajo_valido(tipo = "alumno")
    # Buscar y editar campos seleccionados
    for alumno in alumnos:
        if alumno[0] == id_alumno:
            print(f"\nAlumno encontrado:")
            print(f"1) Nombre: {alumno[3]}")
            print(f"2) Apellido: {alumno[2]}")
            print(f"3) Fecha de nacimiento: {alumno[4]}")

            opcion = input("¿Qué dato desea modificar?: ").strip()

            if opcion == "1":
                alumno[3] = input("Ingrese el nuevo nombre: ")
                alumno[5] = input("Ingrese el nuevo email (ligado al nombre y apellido): ")
            elif opcion == "2":
                alumno[2] = input("Ingrese el nuevo apellido: ")
                alumno[5] = input("Ingrese el nuevo email (ligado al nombre y apellido): ")
            elif opcion == "3":
                alumno[4] = input("Ingrese la nueva fecha de nacimiento (dd-mm-aaaa): ")
            else:
                return

            # Confirmación de cambios
            print()
            print("Dato modificado correctamente.")
            print("Nuevo registro")
            print(f"nombre: {alumno[3]}")
            print(f"apellido: {alumno[2]}")
            print(f"fecha de nacimiento: {alumno[4]}")
            print(f"email: {alumno[5]}")
            return
    print("No se encontró un alumno con ese ID.")
    return

# Listar alumnos
def listar_alumnos():
    if not alumnos:
        print("Sin alumnos.")
        return
    # Encabezado
    print(f"{'LEGAJO':<8}| {'APELLIDO':<17} | {'NOMBRE':<13} | {'EMAIL':<27}")
    print("-" * 70)
    for a in alumnos:
        print(f"{a[AL_LEGAJO]:<6} | {a[AL_APELLIDO]:<15} | {a[AL_NOMBRE]:<12} | {a[AL_EMAIL]:<30}")
    print()
    return

# Menú de alumnos (loop de opciones)
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
            print("Baja de alumno.")
            baja_alumno(alumnos, alumnos_baja)
        elif opcion == "4":
            print("Modificar alumno.")
            modificar_dato_alumno(alumnos)
    return "volver"
