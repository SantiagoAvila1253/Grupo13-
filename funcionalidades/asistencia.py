# Módulo de lógica de Presentismo
"""
Responsabilidades:
- Sincronizar el archivo CSV de asistencia con los JSON de alumnos y clases.
- Tomar asistencia completa por clase.
- Modificar asistencia comenzando desde un legajo elegido.
- Actualizar el porcentaje de asistencia en alumnos.json.
"""

# Importaciones
from core import es_json, es_csv, validadores, helpers, estadisticas, menus
from funcionalidades import Reportes, filtros


# Funciones de ordenamiento clase_id, apellido, nombre, legajo

def orden_clase_apellido_nombre_legajo(fila):
    try:
        clase_id = int(fila[0])
        legajo = int(fila[1])
        apellido = fila[2]
        nombre = fila[3]
        return (clase_id, apellido.lower(), nombre.lower(), legajo)
    except Exception:
        return (0, "", "", 0)


# Orden dentro de una clase: apellido, nombre, legajo
def orden_apellido_nombre_legajo(fila):
    try:
        legajo = int(fila[1])
        apellido = fila[2]
        nombre = fila[3]
        return (apellido.lower(), nombre.lower(), legajo)
    except Exception:
        return ("", "", 0)


# Sincronización del CSV desde los JSON
def sincronizar_csv_desde_json():
    """
    - Reconstruye la matriz de asistencia en base a los JSON de alumnos y clases.
    - Agrega alumnos o clases nuevas si aparecen en los JSON.
    - Ordena la matriz resultante por clase, apellido, nombre y legajo.
    """
    try:
        alumnos = es_json.leer_alumnos()
        clases = es_json.leer_clases()  
        matriz_actual = es_csv.leer_asistencia()  # matriz SIN cabecera

        estado_por_clase_legajo = {}
        for fila in matriz_actual:
            try:
                clave = (int(fila[0]), int(fila[1]))
                estado_por_clase_legajo[clave] = fila[4]
            except Exception:
                continue

        nuevas_filas = []
        ids_clase = sorted(int(cid) for cid in clases.keys())
        ids_alumno = sorted(int(aid) for aid in alumnos.keys())

        for cid in ids_clase:
            for aid in ids_alumno:
                alumno = alumnos[str(aid)]
                if not alumno.get("activo", True):
                    continue
                apellido = alumno.get("apellido", "").strip()
                nombre = alumno.get("nombre", "").strip()
                estado = estado_por_clase_legajo.get((cid, aid), "")
                nuevas_filas.append([str(cid), str(aid), apellido, nombre, estado])

        nuevas_filas.sort(key=orden_clase_apellido_nombre_legajo)
        es_csv.guardar_asistencia_sobrescribir(nuevas_filas)

        print("Sincronización de asistencia completada correctamente.")
        es_json.pausa()
        return

    except Exception as error:
        print(
            f"No se pudo sincronizar la asistencia. "
            f"Tipo de error: {type(error).__name__}. Detalle: {error}"
        )
        es_json.pausa()
        return


# Toma de asistencia por clase
def tomar_asistencia_por_clase(id_clase):
    """
    - Muestra los alumnos en orden alfabético.
    - Pide ingresar el estado (P/AJ/AI o Enter para no modificar).
    - Guarda los cambios al finalizar y actualiza el porcentaje de asistencia.
    """
    try:
        clases = es_json.leer_clases()
        if not validadores.validar_id_clase_existente(id_clase, clases):
            print("No se pudo ejecutar la acción. Motivo: la clase indicada no existe.")
            es_json.pausa()
            return

        matriz = es_csv.leer_asistencia()
        filas_clase = [f for f in matriz if f and f[0].isdigit() and int(f[0]) == int(id_clase)]

        if not filas_clase:
            print("No hay registros de asistencia para esta clase.")
            es_json.pausa()
            return

        filas_clase.sort(key=orden_apellido_nombre_legajo)
        estado_editado_por_legajo = {}

        print(f"\n--- Tomar asistencia | Clase {id_clase} ---")
        for fila in filas_clase:
            _, legajo, apellido, nombre, estado_actual = fila
            etiqueta = f"{apellido}, {nombre} (Legajo {legajo})"
            print(f"- {etiqueta} | Actual: '{estado_actual or ' '}'")

            while True:
                estado_nuevo = input("Ingresá estado [P/AJ/AI] o Enter para no cambiar: ").strip().upper()
                if estado_nuevo == "":
                    break
                if validadores.validar_estado_asistencia(estado_nuevo):
                    estado_editado_por_legajo[int(legajo)] = estado_nuevo
                    break
                print("Estado inválido. Ingresá P, AJ, AI o Enter para dejar sin cambios.")

        if estado_editado_por_legajo:
            # Aplicar cambios en la matriz completa (para conservar orden global y luego sobrescribir)
            for fila in matriz:
                if fila and fila[0].isdigit() and int(fila[0]) == int(id_clase):
                    leg = int(fila[1]) if fila[1].isdigit() else None
                    if leg in estado_editado_por_legajo:
                        fila[4] = estado_editado_por_legajo[leg]

            matriz.sort(key=orden_clase_apellido_nombre_legajo)
            es_csv.guardar_asistencia_sobrescribir(matriz)
            estadisticas.recalcular_y_guardar_porcentajes()

            print("Asistencia guardada correctamente y porcentajes actualizados.")
            es_json.pausa()
            return

        print("No hubo cambios para guardar.")
        es_json.pausa()
        return

    except Exception as error:
        print(
            f"No se pudo tomar asistencia. "
            f"Tipo de error: {type(error).__name__}. Detalle: {error}"
        )
        es_json.pausa()
        return


# Modificación de asistencia desde un legajo
def modificar_asistencia(id_clase, legajo_inicio):
    """
    - Recorre los alumnos desde ese punto y permite cambiar sus estados.
    - Opción de continuar desde el principio hasta el alumno anterior al inicial.
    """
    try:
        clases = es_json.leer_clases()
        if not validadores.validar_id_clase_existente(id_clase, clases):
            print("No se pudo ejecutar la acción. Motivo: la clase indicada no existe.")
            es_json.pausa()
            return

        alumnos = es_json.leer_alumnos()
        if not validadores.validar_legajo_existente(legajo_inicio, alumnos):
            print("No se pudo ejecutar la acción. Motivo: el legajo indicado no existe.")
            es_json.pausa()
            return

        matriz = es_csv.leer_asistencia()
        filas_clase = [f for f in matriz if f and f[0].isdigit() and int(f[0]) == int(id_clase)]
        if not filas_clase:
            print("No hay registros de asistencia para esta clase (¿sincronizaste?).")
            es_json.pausa()
            return

        filas_clase.sort(key=orden_apellido_nombre_legajo)
        indices_por_legajo = {int(f[1]): i for i, f in enumerate(filas_clase) if f[1].isdigit()}

        if int(legajo_inicio) not in indices_por_legajo:
            print("El legajo no tiene registro en esta clase. Sincronizá antes de modificar.")
            es_json.pausa()
            return

        idx = indices_por_legajo[int(legajo_inicio)]
        estado_editado_por_legajo = {}

        print(f"\n--- Modificar asistencia | Clase {id_clase} | Desde legajo {legajo_inicio} ---")

        # Primer tramo: desde legajo_inicio hasta el final
        for i in range(idx, len(filas_clase)):
            _, legajo, apellido, nombre, estado_actual = filas_clase[i]
            etiqueta = f"{apellido}, {nombre} (Legajo {legajo})"
            print(f"- {etiqueta} | Actual: '{estado_actual or ' '}'")

            while True:
                estado_nuevo = input("Nuevo estado [P/AJ/AI] o Enter para dejar sin cambios: ").strip().upper()
                if estado_nuevo == "":
                    break
                if validadores.validar_estado_asistencia(estado_nuevo):
                    estado_editado_por_legajo[int(legajo)] = estado_nuevo
                    break
                print("Estado inválido. Ingresá P, AJ, AI o Enter para dejar sin cambios.")

        # Segundo tramo opcional: circular desde inicio hasta legajo previo
        desea_continuar = input("¿Querés continuar desde el principio hasta el alumno previo? (S/N): ").strip().lower()
        if desea_continuar == "s":
            for i in range(0, idx):
                _, legajo, apellido, nombre, estado_actual = filas_clase[i]
                etiqueta = f"{apellido}, {nombre} (Legajo {legajo})"
                print(f"- {etiqueta} | Actual: '{estado_actual or ' '}'")

                while True:
                    estado_nuevo = input("Nuevo estado [P/AJ/AI] o Enter para dejar sin cambios: ").strip().upper()
                    if estado_nuevo == "":
                        break
                    if validadores.validar_estado_asistencia(estado_nuevo):
                        estado_editado_por_legajo[int(legajo)] = estado_nuevo
                        break
                    print("Estado inválido. Ingresá P, AJ, AI o Enter para dejar sin cambios.")

        # Aplicación de los cambios
        if estado_editado_por_legajo:
            for fila in matriz:
                if fila and fila[0].isdigit() and int(fila[0]) == int(id_clase):
                    leg = int(fila[1]) if fila[1].isdigit() else None
                    if leg in estado_editado_por_legajo:
                        fila[4] = estado_editado_por_legajo[leg]

            matriz.sort(key=orden_clase_apellido_nombre_legajo)
            es_csv.guardar_asistencia_sobrescribir(matriz)
            estadisticas.recalcular_y_guardar_porcentajes()

            print("Modificaciones guardadas correctamente y porcentajes actualizados.")
            es_json.pausa()
            return

        print("No hubo cambios para guardar.")
        es_json.pausa()
        return

    except Exception as error:
        print(
            f"No se pudo modificar la asistencia. "
            f"Tipo de error: {type(error).__name__}. Detalle: {error}"
        )
        es_json.pausa()
        return


# Control del flujo del submenú de asistencias.
def gestion_asistencias():
    """
    Opciones:
      0) Volver
      1) Tomar asistencia por clase desde el primer alumno o desde un legajo específico
      2) Modificar registros por clase desde un legajo
      3) Filtrar
      4) Reportes
      9) Cerrar sesión
    """
    try:
        seguir = True
        while seguir:
            # Mostrar menú principal de asistencias
            menus.mostrar_menu_asistencia()
            opcion = input("Elegí una opción: ").strip()

            # Validar opción del menú
            if not validadores.opcion_valida_menu(opcion, {"0", "1", "2", "3", "4", "9"}):
                print("Opción inválida.")
                continue

            if opcion == "0":   # volver
                return "volver"

            if opcion == "9":   # cerrar sesión
                return "logout"

            # Opción 1: Tomar asistencia por clase (con inicio configurable)
            if opcion == "1":
                try:
                    # 1) Validar clase
                    clases_json = es_json.leer_clases()
                    clase_txt = input("Ingresá el ID de clase: ").strip()
                    if not validadores.validar_id_clase_existente(clase_txt, clases_json):
                        print("No se pudo ejecutar la acción. Motivo: la clase indicada no existe.")
                        es_json.pausa()
                        continue
                    id_clase = int(clase_txt)

                    # 2) Elegir modo de inicio
                    modo = input("Ingresá 1 para iniciar desde el primer alumno o 2 para iniciar desde un legajo: ").strip()
                    if modo == "1":
                        # Sincronización + Recorrido completo desde el primer alumno (orden A-Z)
                        sincronizar_csv_desde_json()
                        tomar_asistencia_por_clase(id_clase)
                        continue

                    elif modo == "2":
                        # Desde un legajo específico (edición secuencial circular)
                        sincronizar_csv_desde_json()
                        alumnos_json = es_json.leer_alumnos()
                        legajo_txt = input("Ingresá el legajo desde el que querés iniciar: ").strip()
                        if not validadores.validar_legajo_existente(legajo_txt, alumnos_json):
                            print("No se pudo ejecutar la acción. Motivo: el legajo indicado no existe.")
                            es_json.pausa()
                            continue
                        modificar_asistencia(id_clase, int(legajo_txt))
                        continue

                    else:
                        print("Opción inválida. Debés ingresar 1 o 2.")
                        es_json.pausa()
                        continue

                except Exception as error:
                    print(f"No se pudo tomar asistencia. Tipo de error: {type(error).__name__}. Detalle: {error}")
                    es_json.pausa()
                    continue

            # Opción 2: Modificar registros por clase (arrancando en legajo)
            if opcion == "2":
                
                try:
                    sincronizar_csv_desde_json()
                    clases_json = es_json.leer_clases()
                    clase_txt = input("Ingresá el ID de clase: ").strip()
                    if not validadores.validar_id_clase_existente(clase_txt, clases_json):
                        print("No se pudo ejecutar la acción. Motivo: la clase indicada no existe.")
                        es_json.pausa()
                        continue
                    id_clase = int(clase_txt)

                    alumnos_json = es_json.leer_alumnos()
                    legajo_txt = input("Ingresá el legajo desde el que querés iniciar la modificación: ").strip()
                    if not validadores.validar_legajo_existente(legajo_txt, alumnos_json):
                        print("No se pudo ejecutar la acción. Motivo: el legajo indicado no existe.")
                        es_json.pausa()
                        continue

                    modificar_asistencia(id_clase, int(legajo_txt))
                    continue

                except Exception as error:
                    print(f"No se pudo modificar la asistencia. Tipo de error: {type(error).__name__}. Detalle: {error}")
                    es_json.pausa()
                    continue

            # Opción 3: Filtros (redirige al módulo de filtros)
            if opcion == "3":
                try:
                    # Reportes se encarga de invocar core/filtros según corresponda
                    r = filtros.menu_filtros()
                    if r == "logout":
                        return "logout"
                    # si vuelve, continua en este submenú
                    continue
                except Exception as error:
                    print(f"No se pudo abrir el menú de filtros. Tipo de error: {type(error).__name__}. Detalle: {error}")
                    es_json.pausa()
                    continue

            # Opción 4: Reportes (redirige al módulo de reportes)
            if opcion == "4":
                try:
                    # Reportes se encarga de invocar core/filtros según corresponda
                    r = Reportes.menu_reportes()
                    if r == "logout":
                        return "logout"
                    # si vuelve, continua en este submenú
                    continue
                except Exception as error:
                    print(f"No se pudo abrir el menú de reportes. Tipo de error: {type(error).__name__}. Detalle: {error}")
                    es_json.pausa()
                    continue

    except Exception as error:
        print(f"No se pudo ejecutar la gestión de asistencias. Tipo de error: {type(error).__name__}. Detalle: {error}")
        es_json.pausa()
        return "volver"
