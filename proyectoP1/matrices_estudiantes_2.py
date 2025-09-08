# funciones

# función imprimir matrices -- actualizar
def mostrar_matriz(nombre, matriz):
    print(f"{nombre}:")
    for fila in matriz:
        print(matriz[fila][0], end=" ")
    print()
    return 
def alta_alumno():
    print("Alta de alumno ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    fecha_nac = input("Fecha de nacimiento (dd-mm-aaaa): ")
    email = input("Email: ")

    alumnos.append([nombre, apellido, fecha_nac, email])
    print(f" Alumno {nombre} {apellido} agregado correctamente")

def baja_alumno():
    print("Baja de alumno")
    nombre = input("Nombre del alumno: ")
    apellido = input("Apellido del alumno: ")

    for alumno in alumnos:
        if alumno[0] == nombre and alumno[1] == apellido:
            alumnos.remove(alumno)
            print(f" Alumno {alumno[0]} {alumno[1]} eliminado correctamente.")
            alumno.append(alumnos_baja)
            return
    print(" No se encontró un alumno con ese nombre y apellido.")


asistencia = [[]]

# matrices

# matriz materias
materia = [["Matemática", "Martes", "14:00 - 18:00"]]

# lista clases
clases = ["2025-08-05", "2025-08-12", "2025-08-19", "2025-08-26", "2025-09-02", "2025-09-09", "2025-09-16", "2025-09-23", "2025-09-30", "2025-10-07", "2025-10-14", "2025-10-21", "2025-10-28", "2025-11-04", "2025-11-11", "2025-11-18", "2025-11-25"]

# matriz alumnos

alumnos = [
    ["Juan", "Saltid", "08-09-2007", "jsaltid@uade.edu.ar"],
    ["Pablo", "Altanio", "19-04-2004", "paltanio@uade.edu.ar"],
    ["Marcelo", "Mandeo", "02-12-2007", "mmandeo@uade.edu.ar"],
    ["Mateo", "Fernandez", "16-03-2005", "mfernandez@uade.edu.ar"],
    ["Lucia", "Castro", "17-07-2006", "lucastro@uade.edu.ar"],
    ["Julian", "Martinez", "06-05-2003", "jmartinez@uade.edu.ar"],
    ["Sofia", "Nando", "13-07-2004", "snando@uade.edu.ar"],
    ["Agustina", "Gonzales", "09-03-2007", "agonzales@uade.edu.ar"],
    ["Franchesca", "Ameglio", "11-09-2006", "fameglio@uade.edu.ar"],
    ["Joaquin", "Ayala", "20-08-2007", "jayala@uade.edu.ar" ],
    ["Valentina", "Catillo", "01-02-2005", "vcastillo@uade.edu.ar" ],
    ["Lautaro", "Nuñez", "18-04-2006", "lnuñez@uade.edu.ar" ],
    ["Florencia", "Espinosa", "30-01-2007", "fespinosa@uade.edu.ar" ],
    ["Tomas", "Fuentes", "23-03-2004", "tfuentes@uade.edu.ar" ],
    ["Faustina", "Flores", "12-08-2006", "fflores@uade.edu.ar" ]
]

cantidad_de_filas = len(alumnos)
clases = 17





alumnos_baja = [[]]

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
    print("2 - Elige la opcion 2")
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
            print(f"{id:<5} {fila[0]:<12} | {fila[1]:<15} | {fila[2]:<18} | {fila[3]:<25}")
        codigo = int(input("ingrese 1 para dar de baja o 2 para dar de alta(o -1 para finalizar): "))
        while codigo != 1 and codigo != 2 and codigo != -1:
            codigo = int(input("Ingrese 1 para dar de baja, 2 para dar de alta (-1 para finalizar): "))
            if codigo != 1 and codigo != 2 and codigo != -1:
                print("Error: Debe ingresar 1, 2 o -1.")
        if codigo == 1:
            baja_alumno()
        else:
            alta_alumno()
              
    if  opcion==2:
        print("Has elegido la opcion 2")
        
    elif opcion==3:
        print("Has elegido la opcion 3")
       
    imprimirMenu()   
    opcion=int(input("Ingrese la opcion elegida del menu principal: "))

else:
    print("FIN DEL PROGRAMA")
    

 