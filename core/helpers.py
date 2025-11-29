# Funciones de ayuda integradas
from core import es_json, es_csv, validadores as val


# Valida legajo existente
def pedir_legajo_existente(etiqueta="Legajo"):
    """
    Pide un legajo por input hasta que:
        - sea entero positivo
        - exista como clave en data/alumnos.json
    Devuelve el legajo como int.
    """
    alumnos = es_json.leer_alumnos()  # diccionario de diccionarios
    while True:
        texto = input(f"{etiqueta}: ").strip()
        if not val.validar_numero_entero(texto):
            print(f"{etiqueta} inválido: debe ser un entero.")
            continue
        if not val.validar_legajo_formato(texto):
            print(f"{etiqueta} inválido: debe ser mayor que 0.")
            continue
        if not val.validar_legajo_existente(texto, alumnos):
            print(f"{etiqueta} inexistente: {texto}")
            continue
        return int(texto)


# Valida clase existente
def pedir_id_clase_existente(etiqueta="ID de clase"):
    """
    Pide un id de clase por input hasta que:
        - sea entero positivo
        - exista como clave en data/clases.json
    Devuelve el id de clase como int.
    """
    clases = es_json.leer_clases()
    while True:
        texto = input(f"{etiqueta}: ").strip()
        if not val.validar_numero_entero(texto):
            print(f"{etiqueta} inválido: debe ser un entero.")
            continue
        if not val.validar_id_clase_formato(texto):
            print(f"{etiqueta} inválido: debe ser mayor que 0.")
            continue
        if not val.validar_id_clase_existente(texto, clases):
            print(f"{etiqueta} inexistente: {texto}")
            continue
        return int(texto)


# Entrada segura de contraseña (multiplataforma)
def pedir_password(prompt="Contraseña: "):
    """
    Solicita una contraseña de forma segura, mostrando asteriscos (*) en Windows o
    sin mostrar caracteres en otros sistemas operativos.

    Comportamiento detallado:
    --------------------------
    - La función detecta el sistema operativo usando `sys.platform`.
      Si es Windows, utiliza el módulo `msvcrt` para capturar las teclas una por una
      sin que se impriman en la consola. En otros sistemas usa `getpass.getpass()`.

    - Mientras el usuario escribe:
        * Cada carácter válido se guarda internamente en la variable `password`.
          En pantalla solo se imprime un asterisco (*) para ocultar su valor real.
        * La tecla Backspace (código ASCII `\\x08`) elimina el último carácter
          tanto en la variable como visualmente (borrando un asterisco).
        * La tecla Enter (códigos `\\r` o `\\n`) finaliza el ingreso.
        * La tecla Escape (código `\\x1b`) cancela la operación y devuelve "".

    - `flush=True` fuerza que los asteriscos o los borrados se vean inmediatamente,
      sin esperar a que la consola vacíe su buffer.

    - Al finalizar, la función devuelve el texto REAL ingresado por el usuario
      (sin los asteriscos), que puede luego compararse con una contraseña guardada.

    Ejemplo:
    --------
    Usuario escribe: M, a, r, i, a, Backspace, Enter

        Pantalla muestra: *****
        Valor real devuelto: "Mari"

    Seguridad:
    ----------
    - En ningún momento se imprime la contraseña real.
    - No se almacenan logs ni copias temporales visibles.
    - Es compatible con Windows, Linux y macOS.
    """
    import sys

    # Detección del sistema operativo
    if sys.platform.startswith("win"):
        import msvcrt
        print(prompt, end="", flush=True)
        password = ""

        while True:
            tecla = msvcrt.getch()
            # Tecla Enter: finaliza el ingreso de la contraseña
            if tecla in (b"\r", b"\n"):
                print()
                break
            # Backspace borrar un carácter
            elif tecla == b"\x08":
                if len(password) > 0:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            # ESC cancelar ingreso
            elif tecla == b"\x1b":
                print("\nCancelado.")
                return ""
            # Caso normal: se agrega el nuevo carácter y se muestra un asterisco
            else:
                try:
                    char = tecla.decode("utf-8")
                except UnicodeDecodeError:
                    continue
                password += char
                print("*", end="", flush=True)

        return password

    else:
        # En otros sistemas usa getpass (sin mostrar caracteres)
        import getpass
        return getpass.getpass(prompt)
    


# Filtro booleano con filter + lambda
def filtrar_por_campo_booleano(lista_pares, nombre_campo: str, valor_esperado: bool = True):
    """
    Filtra una lista de tuplas (id, datos_dict) quedándose solo con aquellas
    cuyo diccionario de datos tiene el campo booleano == valor_esperado.

    Parámetros:
    - lista_pares: lista de tuplas (id, datos), donde 'datos' es un dict.
      Ejemplo: [("1001", {"apellido": "Gomez", "activo": True}), ...]
    - nombre_campo: nombre de la clave booleana (por ejemplo 'activo').
    - valor_esperado: valor que debe tener el campo para incluir el elemento.

    Funcionamiento:
    - Cada elemento de lista_pares es una tupla (id, datos).
    - La lambda recibe esa tupla como 'par'.
    - 'par[1]' es el diccionario de datos.
    - par[1].get(nombre_campo, False) obtiene el valor del campo.
    - La lambda devuelve True solo si ese valor coincide con valor_esperado.
    - filter() recorre toda la lista y conserva solo los elementos
      para los que la lambda devuelve True.
    """
    return list(
        filter(
            lambda par: par[1].get(nombre_campo, False) == valor_esperado,
            lista_pares,
        )
    )


# Filtro por prefijo con filter + lambda
def filtrar_por_prefijo_texto(lista_pares, nombre_campo: str, prefijo: str):
    """
    Filtra una lista de tuplas (id, datos_dict) quedándose solo con aquellas
    cuyo campo de texto comienza con el prefijo indicado (sin distinguir mayúsculas).

    Parámetros:
    - lista_pares: lista de tuplas (id, datos), donde 'datos' es un dict.
      Ejemplo: [("1001", {"apellido": "Gomez"}), ("1002", {"apellido": "Martinez"}), ...]
    - nombre_campo: nombre de la clave de texto (por ejemplo 'apellido', 'materia').
    - prefijo: texto de prefijo a comparar (lo normal es que venga de un input).

    Funcionamiento:
    - Se normaliza el prefijo a minúsculas.
    - Cada elemento de lista_pares es una tupla (id, datos).
    - La lambda toma par[1].get(nombre_campo, "") como string,
      lo pasa a minúsculas y verifica si empieza con el prefijo.
    - filter() recorre la lista y conserva solo las tuplas donde
      el campo textual cumple esa condición.
    """
    prefijo = prefijo.lower()
    return list(
        filter(
            lambda par: str(par[1].get(nombre_campo, "")).lower().startswith(prefijo),
            lista_pares,
        )
    )


# Formato de línea de alumno
def formatear_linea_alumno(item_alumno):
    """
    Toma una tupla (legajo_str, datos_dict) de un alumno
    y devuelve un string formateado para listados.
    """
    legajo_str, datos = item_alumno
    estado = "Activo" if datos.get("activo", True) else "Inactivo"
#string formateado con alineación para listados
    return (
        f"Legajo: {legajo_str:<6} | "
        f"Alumno: {datos['apellido']:<12}, {datos['nombre']:<15} | "
        f"DNI: {datos['dni']:<10} | "
        f"Estado: {estado:<9}"
    )


# Listados reutilizables

# Apellido y nobmre en mayúscula
def _nombre_en_mayus(reg):
    """
    Devuelve 'APELLIDO, NOMBRE' en mayúsculas.
    Si falta algún dato, retorna un placeholder seguro.
    """
    ape = str(reg.get("apellido", "")).strip().upper() or "(SIN APELLIDO)"
    nom = str(reg.get("nombre", "")).strip().upper() or "(SIN NOMBRE)"
    return f"{ape}, {nom}"


# Lista alumnos en formato tabla:
def listar_alumnos_resumen(incluir_inactivos=False, imprimir=True, titulo="Alumnos", id_clase=None):
    """
    - Por defecto solo activos. Si incluir_inactivos=True, muestra todos.
    - Orden: Apellido, Nombre, Legajo (numérico)
    - Si imprimir=True, imprime y devuelve None. Si imprimir=False, devuelve el string formateado.
    """
    alumnos = es_json.leer_alumnos()

    # Si se pasa id_clase → construir diccionario de estados previos desde asistencia.csv
    estado_por_legajo = {}
    if id_clase is not None:
        matriz = es_csv.leer_asistencia()
        for fila in matriz:
            if not fila or len(fila) < 5:
                continue
            cid_txt, leg, _ape, _nom, est = fila
            if cid_txt.isdigit() and int(cid_txt) == int(id_clase):
                estado_por_legajo[str(leg)] = str(est).strip().upper()

    items = []
    for legajo, reg in alumnos.items():
        activo = bool(reg.get("activo", True))
        if incluir_inactivos or activo:
            nom = _nombre_en_mayus(reg)
            if id_clase is None:
                col3 = "ACTIVO" if activo else "INACTIVO"
            else:
                col3 = estado_por_legajo.get(str(legajo), "") or "—"
            items.append((str(legajo), nom, col3))

    # Ordenar
    items.sort(key=lambda t: (t[1], int(t[0])))

    # Cabecera
    lineas = []
    lineas.append(f"\n{titulo}")
    lineas.append("-" * 70)
    if id_clase is None:
        lineas.append(f"{'Legajo':<10}{'Apellido, Nombre':<45}{'Estado':<10}")
    else:
        lineas.append(f"{'Legajo':<10}{'Apellido, Nombre':<45}{'Asist.':<10}")
    lineas.append("-" * 70)

    # Filas
    for leg, nom, col3 in items:
        lineas.append(f"{leg:<10}{nom:<45}{col3:<10}")

    lineas.append("-" * 70)
    lineas.append(f"Total: {len(items)}")

    salida = "\n".join(lineas)
    if imprimir:
        print(salida)
        return None
    return salida


# Pide S/N y valida estrictamente
def pedir_sn(msg="¿Incluir inactivos? (S/N): "):
    """
    Pide una respuesta S/N y la valida estrictamente.
    Devuelve True si S, False si N.
    """
    resp = input(msg).strip().lower()
    while not val.validar_opcion_sn(resp):
        print("Opción inválida. Ingresá 'S' o 'N'.")
        resp = input(msg).strip().lower()
    return resp == "s"

# Lista clases en formato tabla:
def listar_clases_resumen(imprimir=True, titulo="Clases"):
    """
    - Orden numérico por ID de clase.
    - Muestra: ID, Materia (en mayúsculas), Fecha, Horario.
    """
    clases = es_json.leer_clases()

    items = []
    for cid, datos in clases.items():
        mat = str(datos.get("materia", "")).strip().upper() or "(SIN MATERIA)"
        fecha = str(datos.get("fecha", "")).strip()
        horario = str(datos.get("horario", "")).strip()
        items.append((str(cid), mat, fecha, horario))

    items.sort(key=lambda t: int(t[0]))

    lineas = []
    lineas.append(f"\n{titulo}")
    lineas.append("-" * 80)
    lineas.append(f"{'ID Clase':<10}{'Materia':<35}{'Fecha':<15}{'Horario':<15}")
    lineas.append("-" * 80)
    for cid, mat, fecha, hora in items:
        lineas.append(f"{cid:<10}{mat:<35}{fecha:<15}{hora:<15}")
    lineas.append("-" * 80)
    lineas.append(f"Total: {len(items)}")

    salida = "\n".join(lineas)
    if imprimir:
        print(salida)
        return None
    return salida

