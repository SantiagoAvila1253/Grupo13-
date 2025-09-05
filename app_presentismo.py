# imports
import paq_loguin

# funciones

# función imprimir matrices -- actualizar
def mostrar_matriz(nombre, matriz):
    print(f"{nombre}:")
    for fila in matriz:
        print(fila)

    return

# matrices

# matriz de docentes con credenciales de ingreso como operador del sistema (dni, clave)
usuarios_docentes = [["12345678", "Clave.123"]]

# matriz materias
materia = [["Matemática", "Martes", "14:00 - 18:00"]]

# lista clases
# ??? preguntar cantidad de clases que deberíamos incluir
clases = [
    "2025-08-05",
    "2025-08-12",
    "2025-08-19",
    "2025-08-26",
    "2025-09-02",
    "2025-09-09",
    "2025-09-16",
    "2025-09-23",
    "2025-09-30",
    "2025-10-07",
    "2025-10-14",
    "2025-10-21",
    "2025-10-28",
    "2025-11-04",
    "2025-11-11",
    "2025-11-18",
    "2025-11-25",
]

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
    ["Joaquin", "Ayala", "20-08-2007", "jayala@uade.edu.ar"],
    ["Valentina", "Catillo", "01-02-2005", "vcastillo@uade.edu.ar"],
    ["Lautaro", "Nuñez", "18-04-2006", "lnuñez@uade.edu.ar"],
    ["Florencia", "Espinosa", "30-01-2007", "fespinosa@uade.edu.ar"],
    ["Tomas", "Fuentes", "23-03-2004", "tfuentes@uade.edu.ar"],
    ["Faustina", "Flores", "12-08-2006", "fflores@uade.edu.ar"],
]

# lista estados de asistencia
estado_asistencia = ["Presente", "Ausente justificado", "Ausente injustificado"]

# total ausentes injustificados
total_ausentes_injustificados = []

# lista estados de alumnos
estado_alumnos = ["Activo", "Inactivo"]

# materia / clase / alumno / estado asistencia / total ausentes injustificados / estado alumno
presentismo = [
    [1, 1, 1, 1, 1, 1],
    [1, 1, 2, 1, 1, 1],
    [1, 1, 3, 1, 1, 1],
    [1, 1, 4, 1, 1, 1],
    [1, 2, 1, 1, 1, 1],
    [1, 2, 2, 1, 1, 1],
    [1, 2, 3, 2, 1, 1],
    [1, 2, 4, 1, 1, 1],
]

# programa principal


# estado del sistema:
# estado == 0 usuario salió del sistema
# estado == 1 usuario no logueado (inicio)
# estado == 2 usuario logueado
estado = 1

while estado == 1:
    estado = paq_loguin.login_usuario(usuarios_docentes, estado)

mostrar_matriz(
    "Alumnos",
    alumnos,
)
mostrar_matriz(
    "Materia",
    materia,
)
mostrar_matriz(
    "Clases",
    clases,
)
mostrar_matriz(
    "Asistencias",
    estado_asistencia,
)
