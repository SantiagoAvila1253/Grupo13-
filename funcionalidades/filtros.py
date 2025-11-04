# Módulo: filtros.py
"""
Responsabilidades:
- Mostrar el submenú de filtros (recursivo).
- Filtrar datos de asistencia (CSV), alumnos y clases (JSON).
- Aplicar recursividad en el flujo y en el procesamiento de datos.
"""

from core import es_csv, es_json, validadores, menus
from core.es_json import pausa


# Filtros sobre la matriz de asistencia (CSV)
def filtrar_por_apellido_rec(matriz, prefijo, i=0, acumulado=None):
    # Filtra recursivamente por prefijo de apellido (sin distinguir mayúsculas)
    if acumulado is None:
        acumulado = []
    if i == len(matriz):                       # caso base
        return acumulado

    fila = matriz[i]
    if fila and len(fila) >= 3 and fila[2].lower().startswith(prefijo.lower()):
        acumulado.append(fila)

    return filtrar_por_apellido_rec(           # caso recursivo + reducción del dominio
        matriz, prefijo, i + 1, acumulado
    )


def filtrar_por_legajo_rec(matriz, legajo, i=0, acumulado=None):
    ### Filtra recursivamente por legajo exacto
    if acumulado is None:
        acumulado = []
    if i == len(matriz):                       # caso base
        return acumulado

    fila = matriz[i]
    if fila and len(fila) >= 2 and fila[1].isdigit() and int(fila[1]) == legajo:
        acumulado.append(fila)

    return filtrar_por_legajo_rec(             # caso recursivo + reducción del dominio
        matriz, legajo, i + 1, acumulado
    )


def filtrar_por_estado_rec(matriz, estado, i=0, acumulado=None):
    # Filtra recursivamente por estado (P, AJ, AI)
    if acumulado is None:
        acumulado = []
    if i == len(matriz):                       # caso base
        return acumulado

    fila = matriz[i]
    if fila and len(fila) >= 5 and fila[4].upper() == estado.upper():
        acumulado.append(fila)

    return filtrar_por_estado_rec(             # caso recursivo + reducción del dominio
        matriz, estado, i + 1, acumulado
    )


# Filtros sobre JSON: alumnos
def filtrar_alumnos_por_apellido_rec(dic_alumnos, prefijo, claves=None, acumulado=None):
    # Filtra alumnos cuyo apellido comienza con el prefijo indicado
    if claves is None:
        claves = list(dic_alumnos.keys())
    if acumulado is None:
        acumulado = []
    if not claves:                             # caso base
        return acumulado
    clave = claves[0]
    datos = dic_alumnos[clave]
    if datos.get("apellido", "").lower().startswith(prefijo.lower()):
        acumulado.append((clave, datos))

    return filtrar_alumnos_por_apellido_rec(   # caso recursivo + reducción del dominio
        dic_alumnos, prefijo, claves[1:], acumulado
    )


# Filtros sobre JSON: clases
def filtrar_clases_por_mes_rec(dic_clases, mes, claves=None, acumulado=None):
    # Filtra clases según el mes en su campo 'fecha'
    if claves is None:
        claves = list(dic_clases.keys())
    if acumulado is None:
        acumulado = []

    if not claves:                             # caso base
        return acumulado

    clave = claves[0]
    datos = dic_clases[clave]
    fecha = datos.get("fecha", "")

    # slicing del string de fecha: [5:7] → los dos caracteres del mes
    if len(fecha) >= 7 and fecha[5:7] == mes:
        acumulado.append((clave, datos))

    return filtrar_clases_por_mes_rec(         # caso recursivo + reducción del dominio
        dic_clases, mes, claves[1:], acumulado
    )


# Menú principal de filtros (recursivo)
def menu_filtros():
    try:
        menus.mostrar_submenu_filtrar()
        opcion = input("Elegí una opción: ").strip()

        # Validar opción
        if not validadores.opcion_valida_menu(opcion, {"0","1","2","3","4","5"}):
            print("Opción inválida.")
            pausa()
            return menu_filtros()  # caso recursivo (vuelve a mostrar el menú)

        if opcion == "0":
            return "volver"        # caso base del flujo del menú

        # Filtros de asistencia
        if opcion in {"1", "2", "3"}:
            matriz = es_csv.leer_asistencia()
            if opcion == "1":
                prefijo = input("Prefijo de apellido: ").strip().lower()
                resultado = filtrar_por_apellido_rec(matriz, prefijo)
            elif opcion == "2":
                legajo_txt = input("Legajo exacto: ").strip()
                if not validadores.validar_numero_entero(legajo_txt):
                    print("Legajo inválido.")
                    pausa()
                    return menu_filtros()  # recursivo (reintenta)
                resultado = filtrar_por_legajo_rec(matriz, int(legajo_txt))
            elif opcion == "3":
                estado = input("Estado [P/AJ/AI]: ").strip().upper()
                if not validadores.validar_estado_asistencia(estado):
                    print("Estado inválido.")
                    pausa()
                    return menu_filtros()  # recursivo (reintenta)
                resultado = filtrar_por_estado_rec(matriz, estado)

            print("\n--- Resultados ---")
            for f in resultado:
                print(f"{f[0]} | {f[1]} | {f[2]}, {f[3]} | {f[4]}")
            print(f"Total encontrados: {len(resultado)}")
            pausa()
            return menu_filtros()  # caso recursivo (volver al menú)

        # Filtro de alumnos (JSON)
        if opcion == "4":
            alumnos = es_json.leer_alumnos()
            prefijo = input("Prefijo de apellido: ").strip().lower()
            resultado = filtrar_alumnos_por_apellido_rec(alumnos, prefijo)
            print("\n--- Alumnos filtrados ---")
            for legajo, datos in resultado:
                print(f"{legajo} | {datos.get('apellido')}, {datos.get('nombre')}")
            print(f"Total encontrados: {len(resultado)}")
            pausa()
            return menu_filtros()  # caso recursivo (volver al menú)

        # Filtro de clases (JSON) por mes (usando slicing)
        if opcion == "5":
            clases = es_json.leer_clases()
            mes = input("Ingresá el número de mes (ej. '01' a '12'): ").strip()
            if not (len(mes) == 2 and mes.isdigit() and 1 <= int(mes) <= 12):
                print("Mes inválido. Debe tener formato '01' a '12'.")
                pausa()
                return menu_filtros()  # recursivo (reintenta)
            resultado = filtrar_clases_por_mes_rec(clases, mes)
            print(f"\n--- Clases del mes {mes} ---")
            for cid, datos in resultado:
                fecha = datos.get("fecha", "")
                materia = datos.get("materia", "(sin materia)")
                print(f"{cid} | {materia} | Fecha: {fecha}")
            print(f"Total encontradas: {len(resultado)}")
            pausa()
            return menu_filtros()  # caso recursivo (volver al menú)

    except Exception as error:
        print(f"No se pudo ejecutar el menú de filtros. Tipo de error: {type(error).__name__}. Detalle: {error}")
        pausa()
        return "volver"
