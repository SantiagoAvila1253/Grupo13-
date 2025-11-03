# funcionalidades/asistencia.py
"""
Módulo de lógica de Presentismo (sin menús, sin reportes).

Responsabilidades:
- Sincronizar el archivo CSV de asistencia con los JSON de alumnos y clases.
- Tomar asistencia completa por clase.
- Modificar asistencia comenzando desde un legajo elegido.
- Filtrar datos en memoria para su uso desde los menús o reportes.
- Actualizar el porcentaje de asistencia en alumnos.json.

Convenciones:
- Las operaciones de lectura/escritura se manejan en core/es_json.py y core/es_csv.py.
- Las validaciones se delegan a core/validadores.py y core/helpers.py.
- Los estados válidos son: "P", "AJ", "AI" o vacío ("") para sin marcar.
"""

from core import es_json, es_csv, validadores, helpers, estadisticas
from core.datos import CABECERA_CSV, CSV_SEP
from core.es_json import pausa


# ------------------------------------------------------------
# Funciones de ordenamiento
# ------------------------------------------------------------

def orden_clase_apellido_nombre_legajo(fila):
    """
    Define el ordenamiento general del CSV:
    clase_id, apellido, nombre, legajo
    """
    try:
        clase_id = int(fila[0])
        legajo = int(fila[1])
        apellido = fila[2]
        nombre = fila[3]
        return (clase_id, apellido.lower(), nombre.lower(), legajo)
    except Exception:
        return (0, "", "", 0)


def orden_apellido_nombre_legajo(fila):
    """
    Orden dentro de una clase:
    apellido, nombre, legajo
    """
    try:
        legajo = int(fila[1])
        apellido = fila[2]
        nombre = fila[3]
        return (apellido.lower(), nombre.lower(), legajo)
    except Exception:
        return ("", "", 0)


# ------------------------------------------------------------
# Sincronización del CSV desde los JSON
# ------------------------------------------------------------

def sincronizar_csv_desde_json():
    """
    Reconstruye la matriz de asistencia en base a los JSON de alumnos y clases.
    - Mantiene estados previos si el CSV ya existía.
    - Agrega alumnos o clases nuevas si aparecen en los JSON.
    - Ordena la matriz resultante por clase, apellido, nombre y legajo.
    """
    try:
        alumnos = es_json.leer_alumnos()
        clases = es_json.leer_clases()
        matriz_actual = es_csv.leer_asistencia()

        # índice auxiliar para los estados ya guardados
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
            clase = clases[str(cid)]
            for aid in ids_alumno:
                alumno = alumnos[str(aid)]
                if not alumno.get("activo", True):
                    continue

                apellido = alumno.get("apellido", "").strip()
                nombre = alumno.get("nombre", "").strip()
                estado = estado_por_clase_legajo.get((cid, aid), "")
                nuevas_filas.append([
                    str(cid),
                    str(aid),
                    apellido,
                    nombre,
                    estado
                ])

        nuevas_filas.sort(key=orden_clase_apellido_nombre_legajo)
        es_csv.guardar_asistencia_sobrescribir(nuevas_filas)

        print("Sincronización de asistencia completada correctamente.")
        pausa()
        return

    except Exception as error:
        print(f"No se pudo sincronizar la asistencia. Tipo de error: {type(error).__name__}. Detalle: {error}")
        pausa()
        return


# ------------------------------------------------------------
# Toma de asistencia por clase
# ------------------------------------------------------------

def tomar_asistencia_por_clase(id_clase):
    """
    Permite tomar asistencia completa de una clase:
    - Muestra los alumnos en orden alfabético.
    - Pide ingresar el estado (P/AJ/AI o Enter para no modificar).
    - Guarda los cambios al finalizar y actualiza el porcentaje de asistencia.
    """
    try:
        clases = es_json.leer_clases()
        if not validadores.validar_id_clase_existente(id_clase, clases):
            print("No se pudo ejecutar la acción. Motivo: la clase indicada no existe.")
            pausa()
            return

        matriz = es_csv.leer_asistencia()
        filas_clase = [f for f in matriz if f and f[0].isdigit() and int(f[0]) == int(id_clase)]

        if not filas_clase:
            print("No hay registros de asistencia para esta clase (¿sincronizaste?).")
            pausa()
            return

        filas_clase.sort(key=orden_apellido_nombre_legajo)
        estado_editado_por_legajo = {}

        print(f"\n--- Tomar asistencia | Clase {id_clase} ---")
        for fila in filas_clase:
            clase_id, legajo, apellido, nombre, estado_actual = fila
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
            for fila in matriz:
                if fila and fila[0].isdigit() and int(fila[0]) == int(id_clase):
                    leg = int(fila[1]) if fila[1].isdigit() else None
                    if leg in estado_editado_por_legajo:
                        fila[4] = estado_editado_por_legajo[leg]

            matriz.sort(key=orden_clase_apellido_nombre_legajo)
            es_csv.guardar_asistencia_sobrescribir(matriz)
            estadisticas.recalcular_y_guardar_porcentajes()

            print("Asistencia guardada correctamente y porcentajes actualizados.")
            pausa()
            return

        print("No hubo cambios para guardar.")
        pausa()
        return

    except Exception as error:
        print(f"No se pudo tomar asistencia. Tipo de error: {type(error).__name__}. Detalle: {error}")
        pausa()
        return


# ------------------------------------------------------------
# Modificación de asistencia desde un legajo
# ------------------------------------------------------------

def modificar_asistencia(id_clase, legajo_inicio):
    """
    Permite modificar la asistencia de una clase comenzando desde un legajo elegido.
    - Recorre los alumnos desde ese punto y permite cambiar sus estados.
    - Opción de continuar desde el principio hasta el alumno anterior al inicial.
    """
    try:
        clases = es_json.leer_clases()
        if not validadores.validar_id_clase_existente(id_clase, clases):
            print("No se pudo ejecutar la acción. Motivo: la clase indicada no existe.")
            pausa()
            return

        alumnos = es_json.leer_alumnos()
        if not helpers.validar_legajo_existente(legajo_inicio, alumnos):
            print("No se pudo ejecutar la acción. Motivo: el legajo indicado no existe.")
            pausa()
            return

        matriz = es_csv.leer_asistencia()
        filas_clase = [f for f in matriz if f and f[0].isdigit() and int(f[0]) == int(id_clase)]
        if not filas_clase:
            print("No hay registros de asistencia para esta clase (¿sincronizaste?).")
            pausa()
            return

        filas_clase.sort(key=orden_apellido_nombre_legajo)
        indices_por_legajo = {int(f[1]): i for i, f in enumerate(filas_clase) if f[1].isdigit()}

        if int(legajo_inicio) not in indices_por_legajo:
            print("El legajo no tiene registro en esta clase. Sincronizá antes de modificar.")
            pausa()
            return

        idx = indices_por_legajo[int(legajo_inicio)]
        estado_editado_por_legajo = {}

        print(f"\n--- Modificar asistencia | Clase {id_clase} | Desde legajo {legajo_inicio} ---")

        # Primer tramo: desde legajo_inicio hasta el final
        for i in range(idx, len(filas_clase)):
            clase_id, legajo, apellido, nombre, estado_actual = filas_clase[i]
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
                clase_id, legajo, apellido, nombre, estado_actual = filas_clase[i]
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
            pausa()
            return

        print("No hubo cambios para guardar.")
        pausa()
        return

    except Exception as error:
        print(f"No se pudo modificar la asistencia. Tipo de error: {type(error).__name__}. Detalle: {error}")
        pausa()
        return


# ------------------------------------------------------------
# Funciones de filtrado
# ------------------------------------------------------------

def obtener_matriz_asistencia():
    """
    Devuelve la matriz completa (sin cabecera) para los menús o reportes.
    """
    try:
        return es_csv.leer_asistencia()
    except Exception as error:
        print(f"No se pudo obtener la asistencia. Tipo de error: {type(error).__name__}. Detalle: {error}")
        pausa()
        return []


def filtrar_por_apellido(matriz, prefijo):
    """
    Devuelve las filas cuyo apellido comienza con el prefijo indicado (sin distinguir mayúsculas).
    """
    try:
        p = (prefijo or "").strip().lower()
        if not p:
            return list(matriz)
        return [f for f in matriz if f and f[2].lower().startswith(p)]
    except Exception:
        return []


def filtrar_por_legajo(matriz, legajo):
    """
    Devuelve las filas cuyo legajo coincide exactamente con el indicado.
    """
    try:
        leg = int(legajo)
        return [f for f in matriz if f and f[1].isdigit() and int(f[1]) == leg]
    except Exception:
        return []


def filtrar_por_estado(matriz, estado):
    """
    Devuelve las filas cuyo estado coincide con el valor indicado (P, AJ, AI).
    Si 'estado' está vacío, devuelve la matriz completa.
    """
    try:
        e = (estado or "").strip().upper()
        if e == "":
            return list(matriz)
        if not validadores.validar_estado_asistencia(e):
            return []
        return [f for f in matriz if f and len(f) >= 5 and f[4].upper() == e]
    except Exception:
        return []
