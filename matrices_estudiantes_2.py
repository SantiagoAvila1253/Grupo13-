
Alumnos = [
    [1, "Juan", "Saltid" "18", "juan@uade.edu.ar"],
    [2, "Pablo", "Altanio", "20", "pablo@uade.edu.ar"],
    [3, "Marcelo", "Mandeo", "21", "marcelo@uade.edu.ar"],
    [4, "Mateo", "Fernandez", "19", "mateo@uade.edu.ar"],
    [5, "Lucia","Castro", "18", "lucia@uade.edu.ar"],
]

clases = [
    [1, "Matemática", "2025-08-01", "10:00"],
    [2, "Programación", "2025-08-02", "14:00"],
    [3, "biologia", "2025-08-03", "12:00"],
    [4, "ciencias sociales", "2025-08-04", "13:00"],
    [5, "ciencias naturales", "2025-0i8-04", "11:00"],
]

asistencias = [
    [1, 1, 1, "Presente"],
    [2, 2, 1, "Ausente"],
    [3, 3, 2, "Presente"],
    [4, 4, 4, "presente"],
    [5, 5, 3, "ausente"],
]


def mostrar_matriz(nombre, matriz):
    print(f"{nombre}:")
    for fila in matriz:
        print(fila)


#Programa principal 
mostrar_matriz("Alumnos", Alumnos,)
mostrar_matriz("Clases", clases)
mostrar_matriz("Asistencias", asistencias)
