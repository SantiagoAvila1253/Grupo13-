# imports
import login

# funciones

# función imprimir matrices -- actualizar
def mostrar_matriz(nombre, matriz):
    print(f"{nombre}:")
    for fila in matriz:
        print(fila)

    return

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
