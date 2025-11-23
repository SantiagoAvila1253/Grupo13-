# Módulo de ABM de alumnos:
# - Alta (nuevo / reactivar)
# - Baja lógica
# - Modificación de datos
# - Listado y menú de alumnos
# Integra validaciones (regex) y normaliza entradas antes de operar.
 
from core import (validadores as val, es_json, helpers)
from core.datos import ESTADOS_ALUMNO, AL_ACTIVO, AL_INACTIVO, ID_ALUMNO_INICIAL
 
from core.menus import mostrar_menu_alumnos
from core.validadores import opcion_valida_menu
   
 
 
def generar_legajo(alumnos_dict):
    """
    Genera un nuevo ID de legajo único .
    Busca el máximo legajo existente y le suma 1.
    Si no hay alumnos, usa el ID inicial.
    """
    if not isinstance(alumnos_dict, dict):
        raise TypeError("alumnos_dict debe ser un diccionario.")

    if not alumnos_dict:
        return ID_ALUMNO_INICIAL
    
    legajos = []
   
    for clave in alumnos_dict.keys():
        try:
            legajos.append(int(clave))
        except ValueError:
            raise ValueError(f"Legajo no numerico: '{clave}'")
 
    return max(legajos) + 1
 
def pedir_datos_alumno(alumnos_dict, legajo_existente=None):
    """
    Pide los datos de un alumno por consola y los valida.
    Requiere el dict de alumnos para generar legajo y validar DNI duplicado.
    """
   
   
 
    if legajo_existente:
        legajo = legajo_existente
        print(f"\n(Modificando datos para el legajo: {legajo})")
        datos_actuales = alumnos_dict.get(str(legajo), {})
    else:
        legajo = generar_legajo(alumnos_dict)
        print(f"\n(Nuevo legajo generado: {legajo})")
        datos_actuales = {}
 
    # --- Pedir Apellido ---
    apellido = ""
    apellido_valido = False
    while not apellido_valido:
        apellido_input = input(f"Apellido [{datos_actuales.get('apellido', '')}]: ").strip()
       
        if not apellido_input and datos_actuales.get('apellido'):
            apellido = datos_actuales.get('apellido')
            apellido_valido = True
        elif val.nom_ape_valido(apellido_input):
            apellido = apellido_input
            apellido_valido = True
        else:
            print("Error: apellido inválido (mínimo 2 letras).")
 
    # --- Pedir Nombre ---
    nombre = ""
    nombre_valido = False
    while not nombre_valido:
        nombre_input = input(f"Nombre [{datos_actuales.get('nombre', '')}]: ").strip()
       
        if not nombre_input and datos_actuales.get('nombre'):
            nombre = datos_actuales.get('nombre')
            nombre_valido = True
        elif val.nom_ape_valido(nombre_input):
            nombre = nombre_input
            nombre_valido = True
        else:
            print("Error: nombre inválido (mínimo 2 letras).")
 
    # --- Pedir DNI ---
    dni = ""
    dni_valido = False
    while not dni_valido:
        dni_input = input(f"DNI [{datos_actuales.get('dni', '')}]: ").strip()
       
        if not dni_input and datos_actuales.get('dni'):
            dni = datos_actuales.get('dni')
            dni_valido = True
       
        elif val.dni_valido(dni_input):
            dni_duplicado = False
            if dni_input != datos_actuales.get('dni'):
                for datos_alumno in alumnos_dict.values():
                    if datos_alumno['dni'] == dni_input:
                        print(f"Error: El DNI {dni_input} ya está registrado para otro alumno.")
                        dni_duplicado = True
           
            if not dni_duplicado:
                dni = dni_input
                dni_valido = True
       
        else:
            print("Error: DNI inválido (debe tener 7 u 8 dígitos).")
 
    # --- Pedir Fecha de Nacimiento ---
    fecha_nac = ""
    fecha_valida = False
    while not fecha_valida:
        fecha_input = input(f"Fecha Nacimiento (dd-mm-aaaa) [{datos_actuales.get('nacimiento', '')}]: ").strip()
       
        if fecha_input == "":
            fecha_nac = datos_actuales.get('nacimiento', '')
            fecha_valida = True

        elif val.fecha_ddmmaaaa_valida(fecha_input):
            fecha_nac = fecha_input
            fecha_valida = True
        else:
            print("Error: formato de fecha (dd-mm-aaaa) o rango (1915-2009) inválido.")
 
    # --- Pedir Email ---
    email = ""
    email_valido = False
    while not email_valido:
        email_input = input(f"Email [{datos_actuales.get('mail', '')}]: ").strip()
       
        if email_input == "":
            email = datos_actuales.get('mail', '')
            email_valido = True
        elif val.email_valido(email_input):
            email = email_input
            email_valido = True
        else:
            print("Error: formato de email inválido.")
 
    # Estado (siempre Activo en alta o modificación)
    activo_actual = datos_actuales.get("activo", True) if legajo_existente else True
    pct_actual    = datos_actuales.get("% asistencia", 0.0)

    return {
        "% asistencia": pct_actual,
        "activo": activo_actual,
        "apellido": apellido,
        "dni": dni,
        "nacimiento": fecha_nac,
        "mail": email,
        "nombre": nombre,

    }
 
def alta_alumno_nuevo():
    """
    Da de alta un NUEVO alumno en el sistema.
 
    """
   
    # 1. LEER EL JSON
    alumnos_dict = es_json.leer_alumnos()
   
    print("\n--- Alta de Alumno Nuevo ---")
 
    # 2. LLAMAR AL ASISTENTE
    nuevo_alumno_datos = pedir_datos_alumno(alumnos_dict)
   
    # 3. AGREGAR AL DICCIONARIO
    nuevo_legajo = generar_legajo(alumnos_dict)
    nuevo_legajo_str = str(nuevo_legajo)
    alumnos_dict[nuevo_legajo_str] = nuevo_alumno_datos


    alumnos_dict[nuevo_legajo_str] = nuevo_alumno_datos

    # 4. GUARDAR EL JSON
    print(f"\nDando de alta al alumno {nuevo_legajo_str}...")
    es_json.guardar_alumnos(alumnos_dict)
 
def baja_alumno():
    """
    Realiza una baja lógica de un alumno (cambia estado a Inactivo).
    1. Lee el JSON.
    2. Pide un legajo que exista (usando el helper).
    3. Confirma y cambia el estado a "Inactivo".
    4. Guarda el JSON.
    """
   
    # 1. LEER
    alumnos_dict = es_json.leer_alumnos()
    if not alumnos_dict:
        print("No hay alumnos cargados en el sistema.")
        return
 
    print("\n--- Baja de Alumno (Lógica) ---")
   
    # 2. PEDIR LEGAJO
    # (El helper 'pedir_legajo_existente' ya se encarga de
    #  leer el JSON y validar que el legajo exista)
    legajo_int = helpers.pedir_legajo_existente("Legajo del alumno a dar de baja")
    legajo_str = str(legajo_int)
 
    # 3. CAMBIAR ESTADO
    # Verificamos el estado actual
    datos_alumno = alumnos_dict[legajo_str]
    if not datos_alumno.get("activo", True):
        print("El alumno ya se encuentra inactivo.")
        input("Presioná Enter para continuar.")
        return
   
    print(f"Alumno a dar de baja: {datos_alumno['apellido']}, {datos_alumno['nombre']}")
   
    # Confirmación
    confirmar = ""
    es_valido = False
    while not es_valido:
        confirmar = input("¿Estás seguro (S/N)?: ").strip().lower()
        es_valido = val.validar_opcion_sn(confirmar)
        if not es_valido:
            print("Opción inválida. Ingresá 'S' o 'N'.")
 
    if confirmar == "n":
        print("Baja cancelada.")
        input("(Presioná Enter para continuar)")
        return
   
    # Actualizamos el estado en el diccionario
    # 4. ACTUALIZAMOS Y GUARDAMOS EL ESTADO EN EL DICCIONARIO
    alumnos_dict[legajo_str]["activo"] = False


    # Guardamos los cambios en el JSON
    print(f"Dando de baja al alumno {legajo_str}...")
    es_json.guardar_alumnos(alumnos_dict)
 

def reactivar_alumno():
    """
    Reactiva a un alumno inactivo (pasa activo=False -> True).
    """
    from core import es_json

    # 1) Leer siempre desde disco
    alumnos_dict = es_json.leer_alumnos()
    if not alumnos_dict:
        print("No hay alumnos cargados en el sistema.")
        return

    print("\n--- Reactivar Alumno Inactivo ---")

    # 2) Filtrar SOLO por 'activo' == False (normalizado)
    alumnos_inactivos = {}
    for legajo, datos in alumnos_dict.items():
        v = datos.get("activo", True)
        if isinstance(v, str):
            v_norm = v.strip().lower() in ("true", "1", "si", "sí")
        else:
            v_norm = bool(v)
        if not v_norm:  # inactivo
            alumnos_inactivos[legajo] = datos

    if not alumnos_inactivos:
        print("No se encontraron alumnos inactivos para reactivar.")
        for leg, d in alumnos_dict.items():
            print(f"  {leg}: {d.get('activo')!r}")
        input("Presioná Enter para continuar")
        return

    # 3) Listar inactivos
    print("Alumnos inactivos disponibles para reactivar:")
    print("-" * 50)
    for legajo, datos in alumnos_inactivos.items():
        print(f"Legajo: {legajo} | {datos['apellido']}, {datos['nombre']}")
    print("-" * 50)

    # 4) Pedir y validar legajo
    while True:
        legajo_str = input("Legajo del alumno a reactivar: ").strip()
        if legajo_str in alumnos_inactivos:
            break
        print(f"Error: el legajo {legajo_str} no es un alumno inactivo válido.")

    # 5) Cambiar estado y guardar (limpiar 'estado' si existiera)
    alumnos_dict[legajo_str]["activo"] = True
    alumnos_dict[legajo_str].pop("estado", None)

    es_json.guardar_alumnos(alumnos_dict)

    datos_alumno = alumnos_dict[legajo_str]
    print(f"Alumno reactivado: {legajo_str} | {datos_alumno['apellido']}, {datos_alumno['nombre']}")
    input("Presioná Enter para continuar")

# Dar de alta un alumno (nuevo o reactivación)
def alta_alumno():
    """
    Menú principal para dar de alta.
    Ofrece la opción de crear un alumno nuevo o reactivar uno inactivo.
    """
    print("\n--- Gestión de Altas de Alumnos ---")
    print("1) Dar de alta a un alumno nuevo")
    print("2) Reactivar a un alumno inactivo")
    print("0) Volver al menú anterior")
   
    opcion = ""
    es_valido = False
   
    # Bucle para validar la opción del menú
    while not es_valido:
        opcion = input("Ingresá una opción: ").strip()
        if opcion in ("1", "2", "0"):
            es_valido = True
        else:
            print("Opción no válida. Ingresá '1', '2' o '0'.")
 
    # Llamar a la función correspondiente
    if opcion == "1":
        # Llama a la función 'alta_alumno_nuevo()' que ya pegamos
        alta_alumno_nuevo()
       
    elif opcion == "2":
        # Llama a la función 'reactivar_alumno()' que ya pegamos
        reactivar_alumno()
       
    elif opcion == "0":
        print("Volviendo al menú de alumnos...")
        return # Simplemente vuelve
 
 
# Reactivar un alumno previamente dado de baja
 
# M
 
# Listar alumnos
def listar_alumnos():
    """
    Muestra un listado de todos los alumnos (activos e inactivos).
    Ordenados por Apellido y Nombre, usando MAP y el HELPER.
    """
   
    # 1. LEER
    alumnos_dict = es_json.leer_alumnos()
 
    if not alumnos_dict:
        print("No hay alumnos cargados en el sistema.")
        return
 
    print("\n--- Listado de Alumnos (Ordenado por Apellido y Nombre) ---")
   
    # 2. ORDENAR
    items_ordenados = sorted(
        alumnos_dict.items(),
        key=lambda item: (item[1]['apellido'].lower(), item[1]['nombre'].lower())
    )
 
    # 3. MAPEAR Y UNIR (Llamando al helper)
   
    mapa_de_strings = map(helpers.formatear_linea_alumno, items_ordenados)
   
    listado_completo = "\n".join(mapa_de_strings)
   
   
    print(listado_completo)
   
    input("\n(Presioná Enter para continuar)")
def modificar_dato_alumno():
    """
    Modifica los datos de un alumno existente.
    1. Lee el JSON.
    2. Pide un legajo existente.
    3. Llama al 'helper' pedir_datos_alumno (en modo modificación).
    4. Actualiza el diccionario.
    5. Guarda el JSON.
    """
   
    # 1. LEER
    alumnos_dict = es_json.leer_alumnos()
    if not alumnos_dict:
        print("No hay alumnos cargados en el sistema.")
        return
 
    print("\n--- Modificación de Alumno ---")
   
    # 2. PEDIR LEGAJO
    # (El helper se encarga de validar que exista)
    legajo_int = helpers.pedir_legajo_existente("Legajo del alumno a modificar")
    legajo_str = str(legajo_int)
 
    # Mostramos datos actuales antes de empezar
    print(f"Datos actuales: {alumnos_dict[legajo_str]['apellido']}, {alumnos_dict[legajo_str]['nombre']} | DNI: {alumnos_dict[legajo_str]['dni']}")
    print("(Dejá el campo vacío y presioná Enter para mantener el dato actual)")
 
    # 3. LLAMAR AL ASISTENTE (en modo Modificación)
    #    Le pasamos el diccionario Y el legajo.
    #    Esto le dice a 'pedir_datos_alumno' que está modificando
    #    y que debe mostrar los datos actuales.
    datos_modificados = pedir_datos_alumno(alumnos_dict, legajo_existente=legajo_int)
   
    # 4. ACTUALIZAR EL DICCIONARIO
    alumnos_dict[legajo_str] = datos_modificados
   
    # 5. GUARDAR
    print(f"\nModificando datos del alumno {legajo_str}...")
    es_json.guardar_alumnos(alumnos_dict)
# Menú de alumnos (loop de opciones)
def menu_alumnos():
    """
    Menú de alumnos (loop de opciones).
    Llama a las funciones conectadas al JSON.
    """
    en_alumnos = True
    while en_alumnos:
        mostrar_menu_alumnos() # Esta función es de core.menus
        opcion = input("Elegí una opción: ").strip()
       
        if not opcion_valida_menu(opcion, {"0", "1", "2", "3", "4", "9"}):
            print("Opción inválida.")
            input("(Presioná Enter para continuar)")
           
        elif opcion == "0":
            en_alumnos = False
           
        elif opcion == "9":
            return "logout"  # Para cerrar sesión
           
        elif opcion == "1":
            # Llama a la nueva 'listar_alumnos' (la que usa map)
            listar_alumnos()
           
        elif opcion == "2":
            # Llama al nuevo menú 'alta_alumno' (Bloque 5)
            alta_alumno()
           
        elif opcion == "3":
            # Llama a la nueva 'baja_alumno' (Bloque 3)
            baja_alumno()
           
        elif opcion == "4":
            # Llama a la nueva 'modificar_dato_alumno' (Bloque 6)
            modificar_dato_alumno()
           
    return "volver"  # Para volver al menú principal