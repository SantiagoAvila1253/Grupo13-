# Reportes de asistencia:
# - Por estudiante
# - Global
# - Por todos los alumnos (batch)
# - Por clase
# - Menú de reportes (loop interactivo)

# funcionalidades/reportes.py
# Reportes conectados a data/ vía core/es_json y core/es_csv

from core import es_csv, es_json, menus, validadores, helpers


# centraliza la carga de datos, existe para evitar repetir lecturas en cada reporte
def _cargar_datos_basicos():
    alumnos = es_json.leer_alumnos()  # dict[str -> dict]
    clases = es_json.leer_clases()
    matriz = es_csv.leer_asistencia()  # lista de listas (sin cabecera)
    return alumnos, clases, matriz


# devuelve el total de clases registradas
def _total_clases(clases):
    return len(clases)


# Su objetivo es dar un panorama global del CSV, cuantos presentes hay sobre el total y el porcentaje
def reporte_asistencia_general():
    _, _, matriz = _cargar_datos_basicos()
    # el guion bajo indica que no se usa la variable
    total = len(matriz)
    presentes = sum(
        1 for f in matriz if len(f) >= 5 and str(f[4]).strip().upper() == "P"
    )
    porcentaje = (presentes / total * 100) if total else 0.0
    return f"Asistencia global: {presentes}/{total} registros ({porcentaje:.2f}%)"


# Su objetivo es listar por cada clase quienes estuvieron presentes
def presentes_por_clase():
    alumnos, clases, matriz = _cargar_datos_basicos()

    # indexamos alumnos por legajo (string)
    idx_alumnos = {k: v for k, v in alumnos.items()}
    # Crea un diccionario auxiliar donde la clave es el legajo (string) y el valor es todo el registro del alumno.
    # agrupamos por clase_id
    presentes_por_cid = {}
    for fila in matriz:
        if len(fila) < 5:
            continue
        cid, legajo, _, _, estado = fila
        if str(estado).strip().upper() == "P":
            presentes_por_cid.setdefault(cid, []).append(legajo)

    # setdefault crea una lista vacía si la clase no existe aún en el diccionario

    # armamos salida ordenada por clase
    lineas = []
    for cid in sorted(clases.keys(), key=lambda x: int(x)):
        # el lambda convierte el id de clase a entero para ordenar numéricamente
        datos_clase = clases[cid]
        encabezado = f"Clase {cid} | {datos_clase.get('materia','')} | Fecha: {datos_clase.get('fecha','')} | Horario: {datos_clase.get('horario','')}"
        lineas.append(encabezado)
        legs = presentes_por_cid.get(cid, [])
        if not legs:
            lineas.append("  Presentes (0): ---")
        else:
            lineas.append(f"  Presentes ({len(legs)}):")
            for leg in sorted(legs, key=lambda x: int(x)):
                # los ordena numéricamente por legajo
                reg = idx_alumnos.get(str(leg), {})
                lineas.append(f"    - {helpers._nombre_en_mayus(reg)} (Legajo {leg})")
        lineas.append("")  # línea en blanco
    return "\n".join(lineas)


# Su objetivo es que para cada alumno, calcula su porcentaje de asistencia y lo lista ordenado por Apellido, Nombre
def porcentaje_por_alumno():
    alumnos, clases, matriz = _cargar_datos_basicos()
    total_c = _total_clases(clases)

    # conteo de presentes por legajo
    presentes_por_legajo = {}
    for fila in matriz:
        if len(fila) < 5:
            continue
        _, legajo, _, _, estado = fila
        if estado.upper() == "P":
            presentes_por_legajo[legajo] = presentes_por_legajo.get(legajo, 0) + 1

    # salida ordenada por apellido, nombre
    items = []
    for legajo_str, reg in alumnos.items():
        if total_c == 0:
            pct = 0.0
        else:
            pres = presentes_por_legajo.get(legajo_str, 0)
            pct = (pres / total_c) * 100
        items.append((reg.get("apellido", ""), reg.get("nombre", ""), legajo_str, pct))

    items.sort(key=lambda t: (t[0].lower(), t[1].lower()))
    # ordena por apellido y nombre, ignorando mayúsculas/minúsculas
    lineas = []
    for ape, nom, leg, pct in items:
        reg_min = {"apellido": ape, "nombre": nom}
        lineas.append(f"{helpers._nombre_en_mayus(reg_min)} (Legajo {leg}): {pct:.2f}%")
    return "\n".join(lineas)


# Muestra el Top 5 de alumnos con más inasistencias.
def top_5_inasistencias():
    alumnos = es_json.leer_alumnos()
    if not alumnos:
        print("No hay alumnos cargados en el sistema.")
        return

    # Convertir el diccionario en una lista de tuplas (legajo, datos)
    lista_alumnos = list(alumnos.items())

    # Ordenar de menor a mayor porcentaje de asistencia (más inasistencias primero)
    lista_ordenada = sorted(
        lista_alumnos, key=lambda item: float(item[1].get("% asistencia", 0))
    )

    top_5 = lista_ordenada[:5]

    print("\nTop 5 alumnos con más inasistencias")
    print("-" * 65)
    print(f"{'Legajo':<10}{'Apellido':<18}{'Nombre':<18}{'% Asistencia':>15}")
    print("-" * 65)

    for legajo, datos in top_5:
        pct = float(datos.get("% asistencia", 0))
        print(f"{legajo:<10}{datos['apellido']:<18}{datos['nombre']:<18}{pct:>13.2f}%")

    print("-" * 65)


# --- Menú de reportes ---


def menu_reportes():
    en_reportes = True
    while en_reportes:
        menus.mostrar_menu_reportes()
        opcion = input("\nElegí una opción: ").strip()
        if not validadores.opcion_valida_menu(opcion, {"0", "1", "2", "3", "4", "9"}):
            print("Opción inválida.")
            continue
        if opcion == "0":
            en_reportes = False
        elif opcion == "9":
            return "logout"
        elif opcion == "1":
            print(reporte_asistencia_general())
        elif opcion == "2":
            print(presentes_por_clase())
        elif opcion == "3":
            print(porcentaje_por_alumno())
        elif opcion == "4":
            top_5_inasistencias()
    return "volver"
