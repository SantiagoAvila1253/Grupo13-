# Funciones de ayuda

# Validar legajo
def legajo_valido(tipo): # tipo clase, alumno o inactivo
    # Import local para evitar import circular
    from core.datos import alumnos, alumnos_baja, clases, AL_LEGAJO, CL_ID
    # variables
    if tipo == "alumno":
        dataset = alumnos
        indice = AL_LEGAJO
        etiqueta = "Legajo"
    elif tipo == "clase":
        dataset = clases
        indice = CL_ID
        etiqueta = "ID de clase"
    elif tipo == "inactivo":
        dataset = alumnos_baja
        indice = AL_LEGAJO
        etiqueta = "Legajo"
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
            # Verificar existencia recorriendo la lista correspondiente
            for fila in dataset:
                if fila[indice] == id_num:
                    return id_num  # OK válido y existe
            # Si no se encontró, no existe
            raise KeyError(f"{etiqueta} inexistente: {id_num}")
        except ValueError as error:
            print(error)
            continue   # vuelve al inicio del while y repregunta
        except KeyError as error:
            print(error)
            continue   # vuelve al inicio del while y repregunta

# Ordenar lista de alumnos    
def listar_alumnos_ordenados(alumnos,AL_APELLIDO,AL_NOMBRE,AL_LEGAJO):
    alumnos_ordenada = list(alumnos)
    alumnos_ordenada.sort(key=lambda alumno: (alumno[AL_APELLIDO].upper(), alumno[AL_NOMBRE].upper(), alumno[AL_LEGAJO]))
    return alumnos_ordenada

# Actualizar lista ordenada
def actualizar_alumnos_ordenada():
    import core
    from core import AL_APELLIDO, AL_NOMBRE, AL_LEGAJO
    core.alumnos_ordenada = listar_alumnos_ordenados(core.alumnos, AL_APELLIDO, AL_NOMBRE, AL_LEGAJO)
    return core.alumnos_ordenada