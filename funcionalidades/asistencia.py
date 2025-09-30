# Importar funciones y datos

from core.datos import (
    clases, alumnos, asistencias,
    ESTADOS_ASISTENCIA, PRESENTE, AUS_J, AUS_I, AL_ACTIVO, AL_INACTIVO, CL_ID, CL_MATERIA, CL_FECHA, CL_DIA, CL_HORARIO, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, AL_ESTADO, AL_DNI, AL_EMAIL
)
from core.menus import (
    mostrar_menu_asistencia
)
from core.validadores import (
    legajo_valido_str, estado_asistencia_valido, opcion_valida_menu
)

# Crear diccionarios de clases por id y de alumnos por legajo
def construir_indices():
    clases_por_id = {fila[CL_ID]: fila for fila in clases}
    alumnos_por_legajo = {fila[AL_LEGAJO]: fila for fila in alumnos}
    return clases_por_id, alumnos_por_legajo

# Copia de alumnos por legajo ordenada por apellido, nombre, legajo
def listar_alumnos_ordenados():
    copia = list(alumnos)
    copia.sort(key=lambda alumno: (alumno[AL_APELLIDO].upper(), alumno[AL_NOMBRE].upper(), alumno[AL_LEGAJO]))
    return copia

# acceder al diccionario. 0/1/2 si hay marca; None si no existe
def estado_de(clase_id, legajo):
    return asistencias.get((clase_id, legajo))

# Upsert de asistencia
def set_asistencia(clase_id, legajo, estado_idx):
    asistencias[(clase_id, legajo)] = estado_idx

# Elimina asistencias[(clase_id,legajo)] si existe
def eliminar_asistencia(clase_id, legajo):
    clave = (clase_id, legajo)
    if clave in asistencias:
        del asistencias[clave]

# Cálculos

# Estadísticas globales de un alumno en todas las clases: presentes, AJ, AI, total, %AI, supera_25 (pct = porcentaje)
def estadisticas_alumno(legajo):
    presentes = 0
    aus_just = 0
    aus_injust = 0
    # Recorrer todas las asistencias cargadas
    for clave, estado in asistencias.items():
        clase_id, leg = clave
        if leg == legajo:
            if estado == PRESENTE:
                presentes += 1
            elif estado == AUS_J:
                aus_just += 1
            elif estado == AUS_I:
                aus_injust += 1
    total = presentes + aus_just + aus_injust
    if total > 0:
        pct_ai = (aus_injust / total) * 100.0
    else:
        pct_ai = 0.0
    supera_25 = pct_ai > 25.0
    return presentes, aus_just, aus_injust, total, pct_ai, supera_25

# Aplica inactivo según % de inasistencias injustificadas (>25%)
def aplicar_desactivacion_por_ausentismo(legajo):
    # obtener estadísticas del alumno
    presentes, aus_justificadas, aus_injustificadas, total, porcentaje_ai, supera_25 = estadisticas_alumno(legajo)
    # recorrer lista de alumnos y actualizar su estado
    for fila in alumnos:
        if fila[AL_LEGAJO] == legajo:
            if supera_25:
                fila[AL_ESTADO] = AL_INACTIVO
            else:
                fila[AL_ESTADO] = AL_ACTIVO
            return

# Muestra por pantalla la lista completa de clases con sus datos principales
def mostrar_lista_de_clases():
    # Encabezado de la tabla
    print("\n--- LISTA DE CLASES ---")
    print("ID    | Materia      | Fecha       | Día     | Horario")
    print("------+--------------+-------------+---------+----------------")
    # Recorrer todas las clases y mostrar cada fila con formato
    for clase in clases:
        id_clase = clase[CL_ID]
        materia = clase[CL_MATERIA]
        fecha = clase[CL_FECHA]
        dia = clase[CL_DIA]
        horario = clase[CL_HORARIO]
        print(f"{id_clase:<5} | {materia:<12} | {fecha:<11} | {dia:<7} | {horario}")

# Muestra los datos de una clase específica (ID, Materia, Fecha, Día, Horario)
def mostrar_encabezado_clase(clase_id):
    # Construir diccionario de clases indexadas por ID
    clases_por_id, _ = construir_indices()
    # Buscar la clase con el ID dado
    fila = clases_por_id.get(clase_id)
    # Si no existe, informar y salir
    if not fila:
        print("Clase no encontrada.")
        return
    # Mostrar los datos de la clase en formato claro
    print("\n=== CLASE ===")
    print(f"ID: {fila[CL_ID]}  |  Materia: {fila[CL_MATERIA]}")
    print(f"Fecha: {fila[CL_FECHA]}  |  Día: {fila[CL_DIA]}  |  Horario: {fila[CL_HORARIO]}")
    return

# Devuelve el texto del estado según el índice. Si el índice no es un entero o está fuera de rango, devuelve "-".
def texto_estado(idx):
    if type(idx) is not int:
        return "-"
    if 0 <= idx < len(ESTADOS_ASISTENCIA):
        return ESTADOS_ASISTENCIA[idx]
    return "-"

# Muestra la tabla de asistencias de una clase
# Columnas: LEGAJO | APELLIDO | NOMBRE | DNI | EMAIL | ESTADO | AJ | AI | %ASISTENCIA
# Aplica filtros por apellido (contiene)

def mostrar_tabla_clase(clase_id, filtro_apellido="", filtro_legajo=None, filtro_estado=None):
    # obtener índices de acceso rápido
    clases_por_id, _ = construir_indices()
    # validar existencia de la clase
    if clase_id not in clases_por_id:
        print("Clase no encontrada.")
        return
    print("\n--- LISTA DE ASISTENCIA ---")
    filtros_txt = []
    # normalizar filtro de apellido a mayúsculas para comparar sin case
    fa_norm = ""
    if isinstance(filtro_apellido, str):
        fa_norm = filtro_apellido.upper()
        if fa_norm != "":
            filtros_txt.append(f"Apellido contiene '{fa_norm}'")
    # normalizar filtro de legajo
    legajo_filtrado = None
    if filtro_legajo is not None:
        s_leg = str(filtro_legajo).strip()
        if s_leg != "" and legajo_valido_str(s_leg):
            legajo_filtrado = int(s_leg)
            filtros_txt.append(f"Legajo == {legajo_filtrado}")
    # filtro de estado: solo si es un int y está dentro de los estados posibles
    if type(filtro_estado) is int and filtro_estado in (PRESENTE, AUS_J, AUS_I):
        filtros_txt.append(f"Estado == {ESTADOS_ASISTENCIA[filtro_estado]}")
    # imprimir línea de filtros
    print("Filtros: " + (" | ".join(filtros_txt) if filtros_txt else "ninguno") + "\n")
    print(f"Estados: 0={ESTADOS_ASISTENCIA[PRESENTE]}, 1={ESTADOS_ASISTENCIA[AUS_J]}, 2={ESTADOS_ASISTENCIA[AUS_I]}")
    # encabezados de tabla
    print("LEGAJO | APELLIDO           | NOMBRE             | DNI       | EMAIL                     | ESTADO        | AJ | AI | %ASIST")
    print("-------+--------------------+--------------------+-----------+---------------------------+---------------+----+----+-------")
    # totales de la clase
    tot_p = 0   # presentes
    tot_aj = 0  # ausentes justificados
    tot_ai = 0  # ausentes injustificados
    # contador de filas que pasan los filtros (para el mensaje de "sin resultados")
    filas_visibles = 0
    # obtener alumnos en orden (apellido/nombre o el criterio que tengan)
    lista = listar_alumnos_ordenados()
    # recorrer alumnos (índice manual para respetar tu estilo)
    i = 0
    n = len(lista)
    while i < n:
        a = lista[i]
        # extraer campos del alumno por índice
        legajo = a[AL_LEGAJO]
        apellido = a[AL_APELLIDO]
        nombre = a[AL_NOMBRE]
        dni = a[AL_DNI]
        email = a[AL_EMAIL]
        # bandera que decide si mostrar la fila según filtros
        mostrar_fila = True
        # filtro por apellido (contains, case-insensitive)
        if fa_norm != "":
            if fa_norm not in apellido.upper():
                mostrar_fila = False
        # filtro por legajo exacto
        if mostrar_fila and legajo_filtrado is not None:
            if legajo != legajo_filtrado:
                mostrar_fila = False
        # estado actual del alumno en esta clase (0/1/2 o None)
        estado_actual = estado_de(clase_id, legajo)
        # filtro por estado
        if mostrar_fila and type(filtro_estado) is int and filtro_estado in (PRESENTE, AUS_J, AUS_I):
            if estado_actual != filtro_estado:
                mostrar_fila = False
        # si la fila pasa los filtros, calculamos métricas e imprimimos
        if mostrar_fila:
            # AJ y AI ACUMULADOS del alumno en TODAS las clases (globales)
            aj = 0
            ai = 0
            total = 0
            # recorremos asistencias globales para este legajo
            # clave: (cid, leg)  valor: est. cid = id de la clase
            for (cid, leg), est in asistencias.items():
                if leg == legajo:
                    total = total + 1
                    if est == AUS_J:
                        aj = aj + 1
                    elif est == AUS_I:
                        ai = ai + 1
            # presentes globales = total - (aj + ai)
            presentes = total - (aj + ai)
            # porcentaje de asistencia global del alumno
            if total > 0:
                pct_asist = (presentes / total) * 100.0
            else:
                pct_asist = 0.0
            # texto del estado actual en esta clase
            if type(estado_actual) is int:
                estado_txt = ESTADOS_ASISTENCIA[estado_actual]
            else:
                estado_txt = "-"
            # imprimir fila del alumno (alineada)
            print(
                f"{legajo:<6} | {apellido:<18} | {nombre:<18} | {dni:<9} | "
                f"{email:<25} | {estado_txt:<13} | {aj:^2} | {ai:^2} | {pct_asist:>6.1f}%"
            )
            # acumular totales de ESTA clase según estado_actual
            if estado_actual == PRESENTE:
                tot_p = tot_p + 1
            elif estado_actual == AUS_J:
                tot_aj = tot_aj + 1
            elif estado_actual == AUS_I:
                tot_ai = tot_ai + 1
            # contar fila visible
            filas_visibles = filas_visibles + 1
        # avanzar al siguiente alumno
        i = i + 1
    # mensaje si ningún alumno pasó los filtros
    if filas_visibles == 0:
        print("(No hay filas para mostrar con los filtros dados.)")
    # pie de tabla con totales de la CLASE
    print("-------+--------------------+--------------------+-----------+---------------------------+---------------+----+----+-------")
    total_clase = tot_p + tot_aj + tot_ai
    print(f"Totales de la clase -> Presentes: {tot_p} | AJ: {tot_aj} | AI: {tot_ai} | Total marcas: {total_clase}")

# mensaje y lista para pedir legajo
def pedir_legajo(mensaje="Ingresá el LEGAJO: "):
    print("\n--- LISTA DE ALUMNOS ---")
    print("LEGAJO | APELLIDO, NOMBRE")
    print("-------+----------------------------")
    for a in listar_alumnos_ordenados():
        print(f"{a[AL_LEGAJO]:<6} | {a[AL_APELLIDO]}, {a[AL_NOMBRE]}")
    print()
    return input(mensaje).strip()

# Acciones, opciones del menú del panel

# Carga secuencial de asistencia: permite elegir legajo de inicio (opcional). Con Enter empieza desde el primero
def registrar_asistencia_secuencial(clase_id, inicio_legajo=None):
    # Orden base de alumnos
    ordenados = listar_alumnos_ordenados()
    # índice de inicio (por defecto, el primero)
    idx_inicio = 0
    if inicio_legajo is not None:
        for i, a in enumerate(ordenados):
            if a[AL_LEGAJO] == inicio_legajo:
                idx_inicio = i
    # iterar alumnos desde idx_inicio
    i = idx_inicio
    n = len(ordenados)
    while i < n:
        a = ordenados[i]
        leg, ape, nom = a[AL_LEGAJO], a[AL_APELLIDO], a[AL_NOMBRE]
        print(f"\n{leg} - {ape}, {nom}")
        print("Estado (0 = Presente, 1 = AJ, 2 = AI, Enter = no cambiar)")
        val = input("Estado: ").strip()
        if val == "":
            i += 1
        elif estado_asistencia_valido(val, {"0","1","2"}):
            set_asistencia(clase_id, leg, int(val))
            aplicar_desactivacion_por_ausentismo(leg)
            i += 1
        else:
            print("Valor inválido. Debe ser 0, 1 o 2. (no se avanzó)")

# Modificar o eliminar un registro
def modificar_o_eliminar_registro(clase_id):
    leg = pedir_legajo()
    if not legajo_valido_str(leg):
        print("Legajo inválido.")
        return
    leg = int(leg)
    actual = estado_de(clase_id, leg)
    print(f"Estado actual: {texto_estado(actual)}")
    print('Nuevo estado (0/1/2) o "E" para eliminar, Enter = sin cambios')
    val = input("Nuevo estado: ").strip().upper()
    if val == "":
        print("Sin cambios."); return
    if val == "E":
        if estado_de(clase_id, leg) is not None:
            eliminar_asistencia(clase_id, leg)
            aplicar_desactivacion_por_ausentismo(leg)
            print("Registro eliminado.")
        else:
            print("No había registro para eliminar.")
        return
    if estado_asistencia_valido(val, {"0", "1", "2"}):
        set_asistencia(clase_id, leg, int(val))
        aplicar_desactivacion_por_ausentismo(leg)
        print("Registro actualizado.")
    else:
        print("Valor inválido.")

# filtros es un dict mutado con claves: {'apellido': str, 'legajo': int|None, 'estado': int|None}
def submenu_filtros(filtros, clase_id):
    en_submenu = True
    while en_submenu:
        print("\n--- FILTROS ---")
        print(f"Apellido actual: {filtros['apellido']!r}")
        print(f"Legajo actual: {filtros['legajo']}")
        print(f"Estado actual: {filtros['estado']}")
        print("a) Filtrar por apellido (vacío = sin filtro)")
        print("b) Filtrar por legajo (número exacto; vacío = sin filtro)")
        print("c) Filtrar por estado (Pes = 0; AJ = 1; AI = 2; vacío = sin filtro)")
        print("d) Limpiar todos los filtros")
        print("0) Volver")
        opcion = input("Elegí: ").strip().lower()
        if not opcion_valida_menu(opcion, {"0", "a", "b", "c", "d"}):
            print("Opción inválida.")
        else:
            if opcion == "0":
                en_submenu = False
            elif opcion == "a":
                texto = input("Texto de apellido (vacío = sin filtro): ").strip()
                filtros["apellido"] = texto
                # mostrar tabla al instante
                mostrar_tabla_clase(
                    clase_id,
                    filtro_apellido=filtros["apellido"],
                    filtro_legajo=filtros["legajo"],
                    filtro_estado=filtros["estado"],
                )
            elif opcion == "b":
                texto = input("Legajo exacto (vacío = sin filtro): ").strip()
                if texto == "":
                    filtros["legajo"] = None
                elif legajo_valido_str(texto):
                    filtros["legajo"] = int(texto)
                else:
                    print("Legajo inválido.")
                mostrar_tabla_clase(
                    clase_id,
                    filtro_apellido=filtros["apellido"],
                    filtro_legajo=filtros["legajo"],
                    filtro_estado=filtros["estado"],
                )
            elif opcion == "c":
                print(f"Estados: 0={ESTADOS_ASISTENCIA[PRESENTE]}, 1={ESTADOS_ASISTENCIA[AUS_J]}, 2={ESTADOS_ASISTENCIA[AUS_I]}")
                texto = input("Estado (0/1/2; vacío = sin filtro): ").strip()
                if texto == "":
                    filtros["estado"] = None
                elif estado_asistencia_valido(texto, {"0", "1", "2"}):
                    filtros["estado"] = int(texto)
                else:
                    print("Estado inválido.")
                mostrar_tabla_clase(
                    clase_id,
                    filtro_apellido=filtros["apellido"],
                    filtro_legajo=filtros["legajo"],
                    filtro_estado=filtros["estado"],
                )
            elif opcion == "d":
                filtros["apellido"] = ""
                filtros["legajo"] = None
                filtros["estado"] = None
                print("Filtros limpiados.")
                mostrar_tabla_clase(
                    clase_id,
                    filtro_apellido=filtros["apellido"],
                    filtro_legajo=filtros["legajo"],
                    filtro_estado=filtros["estado"],
                )

# Muestra una tabla con los totales acumulados de asistencia por alumno
def ver_alumnos_global():
    # Encabezado de la tabla
    print("\n--- ALUMNOS (totales acumulados) ---")
    print("LEGAJO | APELLIDO, NOMBRE           | P  | AJ | AI | Tot | %Asist | %Aus (AI) | ¿>25%?")
    print("-------+-----------------------------+----+----+----+-----+--------+-----------+--------")
    # Recorrer alumnos (ordenados por Apellido, Nombre, Legajo)
    for alumno in listar_alumnos_ordenados():
        legajo = alumno[AL_LEGAJO]
        apellido = alumno[AL_APELLIDO]
        nombre = alumno[AL_NOMBRE]
        # Obtener estadísticas globales del alumno en TODAS las clases
        presentes, ausentes_justificados, ausentes_injustificados, total_clases, porcentaje_ai, supera_25 = estadisticas_alumno(legajo)
        # Calcular % de asistencia (si no hay marcas, 0.0)
        if total_clases > 0:
            porcentaje_asistencia = (presentes / total_clases) * 100.0
        else:
            porcentaje_asistencia = 0.0
        # Imprimir la fila formateada
        print(
            f"{legajo:<6} | "
            f"{apellido}, {nombre:<21} | "
            f"{presentes:^2} | {ausentes_justificados:^2} | {ausentes_injustificados:^2} | "
            f"{total_clases:^3} | "
            f"{porcentaje_asistencia:>6.1f}% | {porcentaje_ai:>7.1f}%  | "
            f"{'SI' if supera_25 else 'NO':^6}"
        )

# Muestra el historial de asistencias de un alumno y sus totales; permite modificación puntual
def ver_historial_y_totales_alumno():
    # Pedir legajo y validar
    leg = pedir_legajo()
    if not legajo_valido_str(leg):
        print("Legajo inválido.")
        return
    leg = int(leg)
    # Encabezado del historial
    print("\n--- HISTORIAL DEL ALUMNO ---")
    print("FECHA       | MATERIA      | ESTADO")
    print("------------+--------------+-----------------")
    # Recorrer todas las clases y mostrar solo las que tienen marca
    hubo_registros = False
    for clase in clases:
        clase_id = clase[CL_ID]
        fecha = clase[CL_FECHA]
        materia = clase[CL_MATERIA]
        estado_idx = estado_de(clase_id, leg)
        if estado_idx is not None:
            estado_txt = ESTADOS_ASISTENCIA[estado_idx]
            print(f"{fecha:<12} | {materia:<12} | {estado_txt}")
            hubo_registros = True
    # Si no hubo registros, informar
    if not hubo_registros:
        print("(No hay registros)")
    # Totales del alumno y porcentajes
    presentes, aj, ai, total, pct_ai, supera = estadisticas_alumno(leg)
    if total > 0:
        pct_as = (presentes / total) * 100.0
    else:
        pct_as = 0.0
    print(
        f"\nTotales -> P:{presentes}  AJ:{aj}  AI:{ai}  Total:{total}  "
        f"%Asist:{pct_as:.1f}%  %Aus(AI):{pct_ai:.1f}%  >25%:{'SI' if supera else 'NO'}"
    )
    # Ofrecer modificación puntual del historial
    opcion = input('¿Modificar un registro puntual? (S/N): ').strip().upper()
    if opcion == "S":
        # Pedir CLASE_ID
        clase_texto = input("CLASE_ID: ").strip()
        if not clase_texto.isdigit():
            print("CLASE_ID inválido.")
            return
        clase_id = int(clase_texto)
        # Pedir nuevo estado o eliminar
        print('Nuevo estado: 0=Presente, 1=AJ, 2=AI, "E"=Eliminar, Enter=sin cambios')
        est = input("Nuevo estado: ").strip().upper()
        # Sin cambios
        if est == "":
            print("Sin cambios.")
            return
        # Eliminar registro si existe
        if est == "E":
            eliminar_asistencia(clase_id, leg)
            aplicar_desactivacion_por_ausentismo(leg)
            print("Registro eliminado.")
            return
        # Cambiar por 0/1/2 si es válido
        if estado_asistencia_valido(est, {"0", "1", "2"}):
            set_asistencia(clase_id, leg, int(est))
            aplicar_desactivacion_por_ausentismo(leg)
            print("Registro actualizado.")
            return
        # Valor inválido
        print("Valor inválido.")

# Entrada principal desde el Menú: muestra lista de clases, pide ID y abre panel
def gestion_asistencias():
    seguir = True
    while seguir:
        # Mostrar menú principal de asistencias
        mostrar_menu_asistencia()
        opcion = input("Elegí una opción: ").strip()
        # Validar opción del menú
        if not opcion_valida_menu(opcion, {"0", "1", "2", "3", "4", "9"}):
            print("Opción inválida.")
        else:
            if opcion == "0":   # volver
                seguir = False
            elif opcion == "9": # cerrar sesión
                return "logout"
            # Opción 1: cargar asistencia por clase
            elif opcion == "1":
                # 1) elegir clase
                mostrar_lista_de_clases()
                clase_txt = input("Ingresá el ID de la clase: ").strip()
                if clase_txt.isdigit():
                    clase_id = int(clase_txt)
                    clases_por_id, _ = construir_indices()
                    if clase_id in clases_por_id:
                        # 2) pedir legajo inicial (Enter = todos)
                        legajo_txt = pedir_legajo("Ingresá legajo inicial (Enter = todos): ")
                        if legajo_txt == "":
                            inicio_param = None
                        else:
                            if not legajo_valido_str(legajo_txt):
                                print("Legajo inválido.")
                                inicio_param = None
                            else:
                                inicio_param = int(legajo_txt)
                        if legajo_txt == "" or legajo_valido_str(legajo_txt):
                            registrar_asistencia_secuencial(clase_id, inicio_legajo=inicio_param)
                    else:
                        print("ID de clase inexistente.")
                else:
                    print("ID inválido.")
            # Opción 2: modificar registros
            elif opcion == "2":
                mostrar_lista_de_clases()
                clase_txt = input("Ingresá el ID de la clase: ").strip()
                if clase_txt.isdigit():
                    modificar_o_eliminar_registro(int(clase_txt))
                else:
                    print("ID inválido.")
            # Opción 3: filtros (y mostrar tabla filtrada)
            elif opcion == "3":
                mostrar_lista_de_clases()
                clase_txt = input("Ingresá el ID de la clase para filtrar: ").strip()
                if clase_txt.isdigit():
                    clase_id = int(clase_txt)
                    filtros = {"apellido": "", "legajo": None, "estado": None}
                    submenu_filtros(filtros, clase_id)
                    mostrar_tabla_clase(
                        clase_id,
                        filtro_apellido=filtros["apellido"],
                        filtro_legajo=filtros["legajo"],
                        filtro_estado=filtros["estado"],
                    )
                else:
                    print("ID inválido.")
            # Opción 4: alumnos global
            elif opcion == "4":
                ver_alumnos_global()
                ver_detalle = input("¿Ver historial de un alumno? (S/N): ").strip().upper()
                if ver_detalle == "S":
                    ver_historial_y_totales_alumno()
            else:
                print("Opción inválida.")