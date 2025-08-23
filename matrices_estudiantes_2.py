Alumnos = [
    [1, "Juan", "Saltid", "08-09-2007", "jsaltid@uade.edu.ar"],
    [2, "Pablo", "Altanio", "19-04-2004", "paltanio@uade.edu.ar"],
    [3, "Marcelo", "Mandeo", "02-12-2007", "mmandeo@uade.edu.ar"],
    [4, "Mateo", "Fernandez", "16-03-2005", "mfernandez@uade.edu.ar"],
    [5, "Lucia", "Castro", "17-07-2006", "lucastro@uade.edu.ar"],
    [6, "Julian", "Martinez", "06-05-2003", "jmartinez@uade.edu.ar"],
    [7, "Sofia", "Nando", "13-07-2004", "snando@uade.edu.ar"],
    [8, "Agustina", "Gonzales", "09-03-2007", "agonzales@uade.edu.ar"],
    [9, "Franchesca", "Ameglio", "11-09-2006", "fameglio@uade.edu.ar"],
    [10, "Joaquin", "Ayala", "20-08-2007", "jayala@uade.edu.ar"],
    [11, "Valentina", "Catillo", "01-02-2005", "vcastillo@uade.edu.ar"],
    [12, "Lautaro", "Nuñez", "18-04-2006", "lnuñez@uade.edu.ar"],
    [13, "Florencia", "Espinosa", "30-01-2007", "fespinosa@uade.edu.ar"],
    [14, "Tomas", "Fuentes", "23-03-2004", "tfuentes@uade.edu.ar"],    [15, "Faustina", "Flores", "12-08-2006", "fflores@uade.edu.ar"],
]

materia = ["Matemática", "Martes" "14:00 - 18:00"]

clases = [
    [1, "2025-08-05"],
    [2,  "2025-08-12"],
    [3,  "2025-08-19"],
    [4,  "2025-08-26"],
    [5,  "2025-09-02"],
    [6,  "2025-09-09"],
    [7,  "2025-00-16"],
    [8,  "2025-09-23"],
    [9,  "2025-09-30"],
    [10,  "2025-10-07"],
    [11,  "2025-10-14"],
    [12,  "2025-10-21"],
    [13,  "2025-10-28"],
    [14,  "2025-11-04"],
    [15,  "2025-11-11"],
    [16,  "2025-11-18"],
    [17,  "2025-11-25"],
]

asistencias = [
    [1, 1, "Presente"],
    [2, 1, "Ausente"],
    [3, 2, "Presente"],
    [4, 4, "presente"],
    [5, 3, "ausente"],
]


def mostrar_matriz(nombre, matriz):
    print(f"{nombre}:")
    for fila in matriz:
        print(fila)


#Programa principal 
mostrar_matriz("Alumnos", Alumnos,)
mostrar_matriz("Materia", materia,)
mostrar_matriz("Clases", clases,)
mostrar_matriz("Asistencias", asistencias,)



