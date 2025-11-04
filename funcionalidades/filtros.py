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
        print(
            f"No se pudo obtener la asistencia. "
            f"Tipo de error: {type(error).__name__}. Detalle: {error}"
        )
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
        return [f for f in matriz if f and len(f) >= 3 and f[2].lower().startswith(p)]
    except Exception:
        return []


def filtrar_por_legajo(matriz, legajo):
    """
    Devuelve las filas cuyo legajo coincide exactamente con el indicado.
    """
    try:
        leg = int(legajo)
        return [f for f in matriz if f and len(f) >= 2 and f[1].isdigit() and int(f[1]) == leg]
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
    
    def menu_filtros():
        return