def mostrar_matriz(nombre, matriz):
    print(f"{nombre}:")
    for fila in matriz:
        print(matriz[fila][0], end=" ")
    print()
    return 
def alta_alumno(alumnos,alumnos_baja):
    print("Alta de alumno ")
    print("1 - Dar de alta a un alumno nuevo")
    print("2 - Reactivar a un alumno existente")
    opcion = int(input("Ingrese la opcion elegida: "))
    
    if opcion ==2:
        if alumnos_baja:
            print("Alumnos inactivos disponibles para reactivar:")
            print(f"{'ID':<5} | {'Nombre':<12} | {'Apellido':<15} | {'Email':<27}")
            print("-" * 75)
            for alumno in alumnos_baja:
               
                print(f"{alumno[4]:<5} | {alumno[0]:<12} | {alumno[1]:<15} | {alumno[3]:<27}")
            id_reactivar = int(input("Ingrese el ID del alumno a reactivar: "))
        reactivar_alumno(id_reactivar ,alumnos, alumnos_baja) 
    elif opcion == 1:  
    
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        fecha_nac = input("Fecha de nacimiento (dd-mm-aaaa): ")
        email = input("Email: ")
    
        nuevo_id = 1001 + len(alumnos) + len(alumnos_baja)#genera el nuevo id sumando el 1001 que es el primero y recorre las otras lista y segun la cantidad se suma 
        alumnos.append([nombre, apellido, fecha_nac, email, nuevo_id])
        print(f" Alumno {nombre} {apellido} agregado correctamente con ID {nuevo_id}.")

    else:
        print("Opcion no valida. Por favor, intente de nuevo.")

    

def baja_alumno(alumnos,alumnos_baja):
    print("Baja de alumno")
    id_alumno = int(input("ingrese el ID del alumno a dar de baja: "))

    for alumno in alumnos:
        if  alumno[4] == id_alumno:
            alumnos_baja.append(alumno)
            alumnos.remove(alumno)
            print(f" Alumno {alumno[0]} {alumno[1]} y ID {id_alumno} eliminado correctamente.")
            return
    print(" No se encontró un alumno con ese ID.")


def reactivar_alumno(id_reactivar, alumnos, alumnos_baja):
    alumno_a_reactivar= list(filter(lambda x:x[4]== id_reactivar, alumnos_baja))

    if alumno_a_reactivar:
        alumnos.append(alumno_a_reactivar[0])
        alumnos_baja.remove(alumno_a_reactivar[0])
        alumnos.sort(key=lambda x: x[1])
        print(f" El alumno con Id {id_reactivar} ha sido reactivado")
    else:
        print(f" No se encontró un alumno con el ID {id_reactivar} en la lista de inactivos.")

#Función para la opción 2:
def modificar_dato_alumno(alumnos):
    print("Modificar datos de un alumno")
    id_alumno = int(input("Ingrese el ID del alumno a modificar: "))

    for alumno in alumnos:
        if alumno[4] == id_alumno:
            print(f"\nAlumno encontrado:")
            print(f"1 - Nombre: {alumno[0]}")
            print(f"2 - Apellido: {alumno[1]}")
            print(f"3 - Fecha de nacimiento: {alumno[2]}")
            print(f"4 - Email: {alumno[3]}\n")

            opcion = int(input("¿Qué dato desea modificar? (1-4): "))

            if opcion == 1:
                alumno[0] = input("Ingrese el nuevo nombre: ")
                alumno[3] = input("Ingrese el nuevo email (ligado al nombre y apellido): ")

            elif opcion == 2:
                alumno[1] = input("Ingrese el nuevo apellido: ")
                alumno[3] = input("Ingrese el nuevo email (ligado al nombre y apellido): ")

            elif opcion == 3:
                alumno[2] = input("Ingrese la nueva fecha de nacimiento (dd-mm-aaaa): ")

            elif opcion == 4:
                alumno[3] = input("Ingrese el nuevo email: ")

            else:
                print("Opción inválida.")
                return
            print()
            print("Dato modificado correctamente.")
            print("Nuevo registro")
            print(f"nombre: {alumno[0]}")
            print(f"apellido: {alumno[1]}")
            print(f"fecha de nacimiento: {alumno[2]}")
            print(f"email: {alumno[3]}")
            
                  
            return
    print("No se encontró un alumno con ese ID.")