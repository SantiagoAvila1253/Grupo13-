# Módulo: filtros.py
"""
Responsabilidades:
- Mostrar el submenú de filtros (recursivo).
- Filtrar datos de asistencia (CSV), alumnos y clases (JSON).
- Aplicar recursividad en el flujo y en el procesamiento de datos.
"""

from core import es_csv, es_json, validadores, menus, helpers
from core.es_json import pausa


# Filtros sobre la matriz de asistencia (CSV)
def filtrar_por_apellido_rec(
    matriz, prefijo, incluir_inactivos=False, i=0, acumulado=None
):
    # Filtra recursivamente por prefijo de apellido (sin distinguir mayúsculas)
    if acumulado is None:
        acumulado = []
    if i == len(matriz):  # caso base
        if incluir_inactivos:
            # Si terminó de recorrer el CSV y se pidió incluir inactivos:
            alumnos = es_json.leer_alumnos()
            clases = es_json.leer_clases()
            ids_clase = sorted(map(int, clases.keys()))
            # legajos presentes en el CSV
            presentes = {int(f[1]) for f in acumulado if f and f[1].isdigit()}
            # Buscar inactivos cuyo apellido sea igual a el prefijo
            pref = prefijo.lower()
            for leg, dat in alumnos.items():
                ape = str(dat.get("apellido", "")).lower()
                if (
                    ape.startswith(pref)
                    and not bool(dat.get("activo", True))
                    and int(leg) not in presentes
                ):
                    ape_out = dat.get("apellido", "")
                    nom_out = dat.get("nombre", "")
                    # Genero una fila por clase (estado vacío)
                    for cid in ids_clase:
                        acumulado.append([str(cid), str(leg), ape_out, nom_out, ""])
        return acumulado

    fila = matriz[i]
    if (
        isinstance(fila, (list, tuple))
        and len(fila) >= 3
        and str(fila[2]).lower().startswith(prefijo.lower())
    ):
        acumulado.append(fila)

    return filtrar_por_apellido_rec(  # caso recursivo + reducción del dominio
        matriz, prefijo, incluir_inactivos, i + 1, acumulado
    )


def filtrar_por_legajo_rec(matriz, legajo, i=0, acumulado=None):
    ### Filtra recursivamente por legajo exacto
    if acumulado is None:
        acumulado = []
    if i == len(matriz):  # caso base
        return acumulado

    fila = matriz[i]
    if fila and len(fila) >= 2 and fila[1].isdigit() and int(fila[1]) == legajo:
        acumulado.append(fila)

    return filtrar_por_legajo_rec(  # caso recursivo + reducción del dominio
        matriz, legajo, i + 1, acumulado
    )


def filtrar_por_estado_rec(matriz, estado, i=0, acumulado=None):
    # Filtra recursivamente por estado (P, AJ, AI)
    if acumulado is None:
        acumulado = []
    if i == len(matriz):  # caso base
        return acumulado

    fila = matriz[i]
    if fila and len(fila) >= 5 and fila[4].strip().upper() == estado.strip().upper():
        acumulado.append(fila)

    return filtrar_por_estado_rec(  # caso recursivo + reducción del dominio
        matriz, estado, i + 1, acumulado
    )


# Filtros sobre JSON: alumnos
def filtrar_alumnos_por_apellido_rec(dic_alumnos, prefijo, claves=None, acumulado=None):
    # Filtra alumnos cuyo apellido comienza con el prefijo indicado
    if claves is None:
        claves = list(dic_alumnos.keys())
    if acumulado is None:
        acumulado = []
    if not claves:  # caso base
        return acumulado
    clave = claves[0]
    datos = dic_alumnos[clave]
    if datos.get("apellido", "").lower().startswith(prefijo.lower()):
        acumulado.append((clave, datos))

    return filtrar_alumnos_por_apellido_rec(  # caso recursivo + reducción del dominio
        dic_alumnos, prefijo, claves[1:], acumulado
    )


# Filtros sobre JSON: clases
def filtrar_clases_por_mes_rec(dic_clases, mes, claves=None, acumulado=None):
    # Filtra clases según el mes en su campo 'fecha'
    if claves is None:
        claves = list(dic_clases.keys())
    if acumulado is None:
        acumulado = []

    if not claves:  # caso base
        return acumulado

    clave = claves[0]
    datos = dic_clases[clave]
    fecha = datos.get("fecha", "")

    # slicing del string de fecha: [5:7] → los dos caracteres del mes
    if len(fecha) >= 7 and fecha[5:7] == mes:
        acumulado.append((clave, datos))

    return filtrar_clases_por_mes_rec(  # caso recursivo + reducción del dominio
        dic_clases, mes, claves[1:], acumulado
    )


# Menú principal de filtros (recursivo)
def menu_filtros():
    try:
        menus.mostrar_menu_filtrar()
        opcion = input("\nElegí una opción: ").strip()

        # Validar opción
        if not validadores.opcion_valida_menu(opcion, {"0", "1", "2", "3", "4", "5"}):
            print("Opción inválida.")
            pausa()
            return menu_filtros()  # caso recursivo (vuelve a mostrar el menú)

        if opcion == "0":
            return "volver"  # caso base del flujo del menú

        # Filtros de asistencia
        if opcion in {"1", "2", "3"}:
            matriz = es_csv.leer_asistencia()
            if opcion == "1":
                matriz = es_csv.leer_asistencia()
                prefijo = input("Prefijo de apellido: ").strip().lower()
                resultado = filtrar_por_apellido_rec(
                    matriz, prefijo, incluir_inactivos=True
                )

                print("\n--- Resultados ---")
                for f in resultado:
                    if not (isinstance(f, (list, tuple)) and len(f) >= 5):
                        continue  # por si se cuela algo raro
                    print(f"{f[0]} | {f[1]} | {f[2]}, {f[3]} | {f[4]}")
                print(f"Total encontrados: {len(resultado)}")
                pausa()
                return menu_filtros()

            elif opcion == "2":
                matriz = es_csv.leer_asistencia()
                inc = helpers.pedir_sn("¿Incluir inactivos? (S/N): ")
                helpers.listar_alumnos_resumen(
                    incluir_inactivos=inc, imprimir=True, titulo="Alumnos disponibles"
                )
                legajo_txt = input("Legajo exacto: ").strip()
                if not validadores.validar_numero_entero(legajo_txt):
                    print("Legajo inválido.")
                    pausa()
                    return menu_filtros()  # recursivo (reintenta)
                legajo = int(legajo_txt)
                resultado = filtrar_por_legajo_rec(matriz, legajo)
                alumnos = es_json.leer_alumnos()
                if not inc:
                    resultado = [
                        (leg, dat)
                        for (leg, dat) in resultado
                        if dat.get("activo", True)
                    ]
                elif not resultado:
                    reg = alumnos.get(str(legajo))
                    # lo que hace es agregar al resultado el alumno inactivo si no tiene registros de asistencia
                    if reg and not reg.get("activo", True):
                        # lee todas las clases de clases.json
                        for cid in sorted(map(int, es_json.leer_clases().keys())):
                            # fabrica una fila por cada clase
                            resultado.append(
                                [
                                    str(cid),
                                    legajo_txt,
                                    reg.get("apellido", ""),
                                    reg.get("nombre", ""),
                                    "",
                                ]
                            )

                print("\n--- Resultados ---")
                for f in resultado:
                    print(f"{f[0]} | {f[1]} | {f[2]}, {f[3]} | {f[4]}")
                print(f"Total encontrados: {len(resultado)}")
                pausa()
                return menu_filtros()

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

        # Filtro de alumnos (JSON): por prefijo de apellido + activos usando helpers con filter()
        if opcion == "4":
            alumnos = es_json.leer_alumnos()  # dict {legajo: datos_dict}
            inc = helpers.pedir_sn("¿Incluir inactivos? (S/N): ")
            helpers.listar_alumnos_resumen(
                incluir_inactivos=inc,
                imprimir=True,
                titulo="Alumnos disponibles",
            )

            prefijo = input("Prefijo de apellido: ").strip()

            # Convertir el diccionario en lista de tuplas (legajo, datos)
            lista_pares = list(alumnos.items())

            # 1) Filtrar por prefijo de apellido (usa filter() internamente)
            resultado = helpers.filtrar_por_prefijo_texto(
                lista_pares,
                nombre_campo="apellido",
                prefijo=prefijo,
            )

            # 2) Si NO se quieren inactivos, filtrar por campo booleano "activo"
            if not inc:
                resultado = helpers.filtrar_por_campo_booleano(
                    resultado,
                    nombre_campo="activo",
                    valor_esperado=True,
                )

            print("\n--- Alumnos filtrados ---")
            for legajo, datos in resultado:
                print(f"{legajo} | {datos.get('apellido')}, {datos.get('nombre')}")
            print(f"Total encontrados: {len(resultado)}")
            pausa()
            return menu_filtros()  # caso recursivo (volver al menú)

    except (ValueError, TypeError, AttributeError, KeyError, RuntimeError) as error:
        print("\nNo se pudo ejecutar el menú de filtros.")
        print(f"Tipo de error: {type(error).__name__}")
        print(f"Detalle: {error}\n")
        pausa()
        return "volver"
