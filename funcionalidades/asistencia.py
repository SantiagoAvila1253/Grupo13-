# importar funciones y variables

from core.datos import (
    clases, alumnos, asistencias,
    ESTADOS_ASISTENCIA, PRESENTE, AUS_J, AUS_I, AL_ACTIVO, AL_INACTIVO, CL_ID, CL_MATERIA, CL_FECHA, CL_DIA, CL_HORARIO, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, AL_ESTADO, AL_DNI, AL_EMAIL,
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

# acceder al diccionario

# 0/1/2 si hay marca; None si no existe

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

# Devuelve los totales de una clase: presentes, ausencias justificadas, ausencias injustificadas y el total

def totales_de_clase(clase_id):
    presentes = 0
    aus_justificadas = 0
    aus_injustificadas = 0

    # recorrer todas las asistencias
    for (clase, legajo), estado in asistencias.items():
        if clase == clase_id:
            if estado == PRESENTE:
                presentes += 1
            elif estado == AUS_J:
                aus_justificadas += 1
            elif estado == AUS_I:
                aus_injustificadas += 1

    # total de registros para esa clase
    total = presentes + aus_justificadas + aus_injustificadas

    return presentes, aus_justificadas, aus_injustificadas, total

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
    # Construir diccionario de clases indexadas por ID para acceso rápido
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


def texto_estado(idx):
    return ESTADOS_ASISTENCIA[idx] if isinstance(idx, int) else "-"

# Muestra la tabla de asistencias de una clase
# Columnas: LEGAJO | APELLIDO | NOMBRE | DNI | EMAIL | ESTADO | AJ | AI | %ASISTENCIA
# Aplica filtros por apellido (contiene)

def mostrar_tabla_clase(clase_id, filtro_apellido="", filtro_legajo=None, filtro_estado=None):
    # obtener índices rápidos
    clases_por_id, _ = construir_indices()

    # validar existencia de clase
    if clase_id not in clases_por_id:
        print("Clase no encontrada.")
        return

    # encabezado general
    print("\n--- LISTA DE ASISTENCIA ---")
    print(
        f"Clase: {clases_por_id[clase_id][CL_MATERIA]} | "
        f"Fecha: {clases_por_id[clase_id][CL_FECHA]} | "
        f"Día: {clases_por_id[clase_id][CL_DIA]} | "
        f"Horario: {clases_por_id[clase_id][CL_HORARIO]}"
    )

    # filtros visibles
    filtros_txt = []
    fa_norm = filtro_apellido.strip().upper() if isinstance(filtro_apellido, str) else ""
    if fa_norm != "":
        filtros_txt.append(f"Apellido CONTAINS '{fa_norm}'")
    if isinstance(filtro_legajo, int):
        filtros_txt.append(f"Legajo == {filtro_legajo}")
    if isinstance(filtro_estado, int) and filtro_estado in (PRESENTE, AUS_J, AUS_I):
        filtros_txt.append(f"Estado == {ESTADOS_ASISTENCIA[filtro_estado]}")
    print("Filtros: " + (" | ".join(filtros_txt) if filtros_txt else "ninguno"))

    # encabezados de tabla
    print("LEGAJO | APELLIDO           | NOMBRE             | DNI       | EMAIL                     | ESTADO        | AJ | AI | %ASIST")
    print("-------+--------------------+--------------------+-----------+---------------------------+---------------+----+----+-------")

    # acumuladores de la clase
    tot_p = 0
    tot_aj = 0
    tot_ai = 0
    filas_visibles = 0

    # lista ordenada para imprimir
    lista = listar_alumnos_ordenados()

    # recorrer alumnos
    i = 0
    n = len(lista)
    while i < n:
        a = lista[i]
        legajo = a[AL_LEGAJO]
        apellido = a[AL_APELLIDO]
        nombre = a[AL_NOMBRE]
        dni = a[AL_DNI]
        email = a[AL_EMAIL]

        # bandera para decidir si mostrar o no la fila
        mostrar_fila = True

        # filtro por apellido (contiene, sin mayúsc/minúsc)
        if mostrar_fila:
            if fa_norm != "":
                if fa_norm not in apellido.upper():
                    mostrar_fila = False

        # filtro por legajo exacto
        if mostrar_fila:
            if filtro_legajo and legajo_valido_str(str(filtro_legajo)):
                filtro_legajo = int(filtro_legajo)
                if legajo != filtro_legajo:
                    mostrar_fila = False

        # estado actual de asistencia en esta clase (0/1/2 o None)
        estado_actual = estado_de(clase_id, legajo)

        # filtro por estado (solo si se pidió)
        if mostrar_fila:
            if isinstance(filtro_estado, int) and filtro_estado in (PRESENTE, AUS_J, AUS_I):
                if estado_actual != filtro_estado:
                    mostrar_fila = False

        # si la fila pasa los filtros, calcular y mostrar
        if mostrar_fila:
            # AJ y AI acumulados del alumno en TODAS las clases
            aj = 0
            ai = 0
            total = 0

            # contar presentes/aj/ai del alumno globalmente
            # (sin 'continue', solo ifs)
            for (cid, leg), est in asistencias.items():
                if leg == legajo:
                    total = total + 1
                    if est == AUS_J:
                        aj = aj + 1
                    elif est == AUS_I:
                        ai = ai + 1

            # presentes = total - (aj + ai)
            presentes = total - (aj + ai)

            # porcentaje de asistencia (sobre total del alumno)
            if total > 0:
                pct_asist = (presentes / total) * 100.0
            else:
                pct_asist = 0.0

            # texto del estado actual
            estado_txt = ESTADOS_ASISTENCIA[estado_actual] if isinstance(estado_actual, int) else "-"

            # imprimir fila
            print(
                f"{legajo:<6} | {apellido:<18} | {nombre:<18} | {dni:<9} | "
                f"{email:<25} | {estado_txt:<13} | {aj:^2} | {ai:^2} | {pct_asist:>6.1f}%"
            )

            # acumular totales de la CLASE (solo si hay marca en esta clase)
            if estado_actual == PRESENTE:
                tot_p = tot_p + 1
            elif estado_actual == AUS_J:
                tot_aj = tot_aj + 1
            elif estado_actual == AUS_I:
                tot_ai = tot_ai + 1

            # contar filas visibles
            filas_visibles = filas_visibles + 1

        # avanzar al siguiente alumno
        i = i + 1

    # si no hay filas visibles con los filtros
    if filas_visibles == 0:
        print("(No hay filas para mostrar con los filtros dados.)")

    # pie de tabla con totales de la clase
    print("-------+--------------------+--------------------+-----------+---------------------------+---------------+----+----+-------")
    total_clase = tot_p + tot_aj + tot_ai
    print(f"Totales de la clase -> Presentes: {tot_p} | AJ: {tot_aj} | AI: {tot_ai} | Total marcas: {total_clase}")


# Acciones, opciones del menú del panel

# Carga secuencial de asistencia: permite elegir legajo de inicio (opcional). Con Enter empieza desde el primero

def registrar_asistencia_secuencial(clase_id):
    inicio = input("Legajo de inicio (Enter = primero): ").strip()
    idx_inicio = 0
    ordenados = listar_alumnos_ordenados()
    if inicio and legajo_valido_str(inicio):
        leg_inicial = int(inicio)
        for i, a in enumerate(ordenados):
            if a[AL_LEGAJO] == leg_inicial:
                idx_inicio = i
                break

    i = idx_inicio
    n = len(ordenados)
    while i < n:
        a = ordenados[i]
        leg = a[AL_LEGAJO]; ape = a[AL_APELLIDO]; nom = a[AL_NOMBRE]
        print(f"\n{leg} - {ape}, {nom}")
        print("Estado (0=Presente, 1=AJ, 2=AI, Enter = no cambiar)")
        val = input("Estado: ").strip()
        if val == "":  # no cambiar
            i = i + 1
        else:
            if estado_asistencia_valido(val, {"0", "1", "2"}):
                set_asistencia(clase_id, leg, int(val))
                aplicar_desactivacion_por_ausentismo(leg)
                i = i + 1
            else:
                print("Valor inválido. Debe ser 0, 1 o 2. (no se avanzó)")

# Modificar o eliminar un registro

def modificar_o_eliminar_registro(clase_id):
    leg = input("LEGAJO (obligatorio): ").strip()
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
    
def submenu_filtros(filtros):
    en_submenu = True
    while en_submenu:
        print("\n--- FILTROS ---")
        print(f"Apellido actual: {filtros['apellido']!r}")
        print(f"Legajo actual: {filtros['legajo']}")
        print(f"Estado actual: {filtros['estado']}")
        print("a) Filtrar por apellido (vacío = sin filtro)")
        print("b) Filtrar por legajo (número exacto; vacío = sin filtro)")
        print("c) Filtrar por estado (0/1/2; vacío = sin filtro)")
        print("d) Limpiar todos los filtros")
        print("0) Volver")
        opcion = input("Elegí: ").strip().lower()

        if opcion == "0":
            en_submenu = False
        elif opcion == "a":
            texto = input("Texto de apellido (vacío = sin filtro): ").strip()
            filtros["apellido"] = texto
        elif opcion == "b":
            texto = input("Legajo exacto (vacío = sin filtro): ").strip()
            if texto == "":
                filtros["legajo"] = None
            elif legajo_valido_str(texto):
                filtros["legajo"] = int(texto)
            else:
                print("Legajo inválido.")
        elif opcion == "c":
            texto = input("Estado (0/1/2; vacío = sin filtro): ").strip()
            if texto == "":
                filtros["estado"] = None
            elif estado_asistencia_valido(texto, {"0","1","2"}):
                filtros["estado"] = int(texto)
            else:
                print("Estado inválido.")
        elif opcion == "d":
            filtros["apellido"] = ""
            filtros["legajo"] = None
            filtros["estado"] = None
        else:
            print("Opción inválida.")

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
    leg = input("LEGAJO (detalle): ").strip()
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

# Panel por clase

# Panel de asistencias para una clase

def panel_asistencias(clase_id):
    # filtros activos en la tabla (por defecto, sin filtros)
    filtros = {"apellido": "", "legajo": None, "estado": None}
    en_panel = True

    while en_panel:
        # Encabezado con datos de la clase seleccionada
        mostrar_encabezado_clase(clase_id)

        # Tabla principal de la clase con filtros aplicados
        # Columnas: LEGAJO | APELLIDO | NOMBRE | DNI | EMAIL | ESTADO | AJ | AI | ¿>25%?
        mostrar_tabla_clase(
            clase_id,
            filtro_apellido=filtros["apellido"],
            filtro_legajo=filtros["legajo"],
            filtro_estado=filtros["estado"],
        )

        # Mostrar menú de asistencias
        mostrar_menu_asistencia()
        opcion = input("Elegí una opción: ").strip()

        # Validación de opción
        if not opcion_valida_menu(opcion, {"0", "1", "2", "3", "4", "9"}):
            print("Opción inválida.")

        # Volver a lista de clases
        elif opcion == "0":
            en_panel = False

        # Cerrar sesión
        elif opcion == "9":
            return "logout"

        # Registrar asistencia secuencial
        elif opcion == "1":
            registrar_asistencia_secuencial(clase_id)

        # Modificar o eliminar registro de asistencia
        elif opcion == "2":
            modificar_o_eliminar_registro(clase_id)

        # Submenú de filtros
        elif opcion == "3":
            submenu_filtros(filtros)

        # Ver listado global de alumnos + detalle de historial
        elif opcion == "4":
            ver_alumnos_global()
            ver_detalle = input("¿Ver historial de un alumno? (S/N): ").strip().upper()
            if ver_detalle == "S":
                ver_historial_y_totales_alumno()

    # Si sale del while, vuelve a lista de clases
    return None


# Entrada principal desde el Menú: muestra lista de clases, pide ID y abre panel

def gestion_asistencias():
    seguir = True
    while seguir:
        mostrar_lista_de_clases()
        print('Opciones: ingresá un ID de clase, "0" para volver, "9" para cerrar sesión.')
        valor = input("Seleccioná la clase: ").strip()

        if opcion_valida_menu(valor, {"0","9"}) or valor.isdigit():
            if valor == "0":
                seguir = False
            elif valor == "9":
                return "logout"
            else:
                clase_id = int(valor)
                clases_por_id, _ = construir_indices()
                if clase_id in clases_por_id:
                    res = panel_asistencias(clase_id)
                    if res == "logout":
                        return "logout"
                else:
                    print("ID de clase inexistente.")
        else:
            print("Entrada inválida. Debe ser un ID de clase, 0 o 9.")
