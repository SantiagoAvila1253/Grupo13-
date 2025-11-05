from . import es_json, es_csv, datos

def recalcular_y_guardar_porcentajes():
    alumnos = es_json.leer_alumnos()
    clases = es_json.leer_clases()
    matriz = es_csv.leer_asistencia()

    total_clases = len(clases) or 1  # evitar división por 0

    presentes_por_legajo = {}
    ai_por_legajo = {}
    for fila in matriz:
        if len(fila) < 5:
            continue
        _, legajo, _, _, estado = fila
        estado = (estado or "").upper()
        if estado == "P":
            presentes_por_legajo[legajo] = presentes_por_legajo.get(legajo, 0) + 1
        elif estado == "AI":
            ai_por_legajo[legajo] = ai_por_legajo.get(legajo, 0) + 1

    # actualizar alumnos
    for legajo_str, reg in alumnos.items():
        pres = presentes_por_legajo.get(legajo_str, 0)
        ai = ai_por_legajo.get(legajo_str, 0)
        pct = round((pres / total_clases) * 100, datos.DECIMALES_PORCENTAJE)
        reg["% asistencia"] = float(f"{pct:.{datos.DECIMALES_PORCENTAJE}f}")

        ai_pct = (ai / total_clases) * 100
        if ai_pct > datos.PORC_MAX_INASISTENCIA:
            reg["activo"] = False

    es_json.guardar_alumnos(alumnos)
