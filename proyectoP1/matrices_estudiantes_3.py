# funciones

# función imprimir matrices -- actualizar
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



# matrices

# matriz materias
materia = [["Matemática", "Martes", "14:00 - 18:00"]]

# lista clases
clases = ["2025-08-05", "2025-08-12", "2025-08-19", "2025-08-26", "2025-09-02", "2025-09-09", "2025-09-16", "2025-09-23", "2025-09-30", "2025-10-07", "2025-10-14", "2025-10-21", "2025-10-28", "2025-11-04", "2025-11-11", "2025-11-18", "2025-11-25"]

# matriz alumnos

alumnos = [
    ["Juan", "Saltid", "08-09-2007", "jsaltid@uade.edu.ar", 1001],
    ["Pablo", "Altanio", "19-04-2004", "paltanio@uade.edu.ar", 1002],
    ["Marcelo", "Mandeo", "02-12-2007", "mmandeo@uade.edu.ar", 1003],
    ["Mateo", "Fernandez", "16-03-2005", "mfernandez@uade.edu.ar", 1004],
    ["Lucia", "Castro", "17-07-2006", "lucastro@uade.edu.ar", 1005],
    ["Julian", "Martinez", "06-05-2003", "jmartinez@uade.edu.ar", 1006],
    ["Sofia", "Nando", "13-07-2004", "snando@uade.edu.ar", 1007],
    ["Agustina", "Gonzales", "09-03-2007", "agonzales@uade.edu.ar", 1008],
    ["Franchesca", "Ameglio", "11-09-2006", "fameglio@uade.edu.ar", 1009],
    ["Joaquin", "Ayala", "20-08-2007", "jayala@uade.edu.ar", 1010],
    ["Valentina", "Catillo", "01-02-2005", "vcastillo@uade.edu.ar", 1011],
    ["Lautaro", "Nuñez", "18-04-2006", "lnuñez@uade.edu.ar", 1012],
    ["Florencia", "Espinosa", "30-01-2007", "fespinosa@uade.edu.ar", 1013],
    ["Tomas", "Fuentes", "23-03-2004", "tfuentes@uade.edu.ar", 1014],
    ["Faustina", "Flores", "12-08-2006", "fflores@uade.edu.ar", 1015]
]

alumnos_baja = []

# lista estados de asistencia
estado_asistencia = ["Presente", "Ausente justificado", "Ausente injustificado"]

# lista estados de alumnos
estado_alumnos = ["Activo","Inactivo"]

# materia / clase / alumno / estado asistencia / estado alumno
presentismo = [
    [1,1,1,1,1],
    [1,1,2,1,1],
    [1,1,3,1,1],
    [1,1,4,1,1],
    [1,2,1,1,1],
    [1,2,2,1,1],
    [1,2,3,2,1],
    [1,2,4,1,1]
]


def imprimirMenu():
    print()
    print("********************************************")
    print("Debe elegir una opcion, solo numeros enteros")
    print("1 - Elige la opcion 1: Dar de baja o de alta a los alumnos")   
    print("2 - Elige la opcion 2: Modificar datos de alumnos")
    print("3 - Elige la opcion 3")
    print("0 - Salir")
    print("********************************************")
    print()
    
    return

def validarOpcionMenu(opcion):
    flag=True
    if opcion!=1 and opcion!=2 and opcion!=3 and opcion!=0: #Se ha ingresado un valor invalido por menu
        flag=False
    
    return flag


    
print("Bienvenido al programa de registro de asistencias")
print()


imprimirMenu()
opcion=int(input("Ingrese la opcion elegida del menu principal: "))

#Comienzo del proceso de las opciones del menu elegidas.

while opcion!=0:

    flagMenu=validarOpcionMenu(opcion)
    while flagMenu == False:
        print("Opcion de menu invalida, vuelva a ingresar...")
        print()
        opcion=int(input("Ingrese la opcion elegida del menu principal: "))
        flagMenu=validarOpcionMenu(opcion)

    if opcion==1:
        print("Has elegido la opcion 1: Dar de baja o de alta alumnos")
        print()
        print(f"{'id':<5} | {'Nombre':<12} | {'Apellido':<15} | {'Fecha de nacimiento':<20} | {'Email':<27}")
        print("-"* 80 )
        id = 0
        for fila in alumnos:
            print(f"{fila[4]:<5} {fila[0]:<12} | {fila[1]:<15} | {fila[2]:<18} | {fila[3]:<25}")
        codigo = int(input("ingrese 1 para dar de baja o 2 para dar de alta(o -1 para finalizar): "))
        while codigo != 1 and codigo != 2 and codigo != -1:
            codigo = int(input("Ingrese 1 para dar de baja, 2 para dar de alta (-1 para finalizar): "))
            if codigo != 1 and codigo != 2 and codigo != -1:
                print("Error: Debe ingresar 1, 2 o -1.")
        if codigo == 1:
            baja_alumno(alumnos, alumnos_baja)
        elif codigo ==2:
            alta_alumno( alumnos, alumnos_baja)
        else:
            print("Operacion cancelada")

    if  opcion==2:
        print("Has elegido la opcion 2: Modificar datos de alumnos")
        print()
        print(f"{'id':<5} | {'Nombre':<12} | {'Apellido':<15} | {'Fecha de nacimiento':<20} | {'Email':<27}")
        print("-"* 80 )
        id = 0
        for fila in alumnos:
            print(f"{fila[4]:<5} {fila[0]:<12} | {fila[1]:<15} | {fila[2]:<18} | {fila[3]:<25}")
        modificar_dato_alumno(alumnos)
    elif opcion==3:
        print("Has elegido la opcion 3: Registro de asistencia")
       
    imprimirMenu()   
    opcion=int(input("Ingrese la opcion elegida del menu principal: "))

else:
    print("FIN DEL PROGRAMA")
    

 