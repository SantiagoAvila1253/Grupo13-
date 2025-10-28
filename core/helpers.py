# Funciones de ayuda

# Validar legajo
def legajo_valido(tipo):  # tipo: "alumno", "clase" o "inactivo"
    # Import local para evitar import circular
    from core.datos import alumnos, alumnos_baja, clases, AL_LEGAJO, CL_ID

    if tipo == "alumno":
        dataset, indice, etiqueta = alumnos, AL_LEGAJO, "Legajo"
    elif tipo == "clase":
        dataset, indice, etiqueta = clases, CL_ID, "ID de clase"
    elif tipo == "inactivo":
        dataset, indice, etiqueta = alumnos_baja, AL_LEGAJO, "Legajo"
    else:
        raise ValueError("Tipo inválido: use 'alumno', 'inactivo' o 'clase'.")

    while True:
        try:
            texto = input(f"{etiqueta}: ")
            if texto is None:
                raise ValueError(f"Entrada vacía. Ingresá {etiqueta.lower()}.")
            texto = texto.strip()
            if texto == "":
                raise ValueError(f"Entrada vacía. Ingresá {etiqueta.lower()}.")
            if not texto.isdigit():
                raise ValueError(f"{etiqueta} inválido: debe ser un entero positivo.")

            id_num = int(texto)
            if id_num <= 0:
                raise ValueError(f"{etiqueta} inválido: debe ser mayor que 0.")

            # Verificar existencia
            for fila in dataset:
                if fila[indice] == id_num:
                    return id_num  # OK válido y existe

            # No se encontró → inexistente
            raise ValueError(f"{etiqueta} inexistente: {id_num}")

        except ValueError as error:
            print(error)
            continue

# Actualizar lista ordenada
def actualizar_alumnos_ordenada():
    import core
    from core import AL_APELLIDO, AL_NOMBRE, AL_LEGAJO
    core.alumnos_ordenada = actualizar_alumnos_ordenada(core.alumnos, AL_APELLIDO, AL_NOMBRE, AL_LEGAJO)
    return core.alumnos_ordenada