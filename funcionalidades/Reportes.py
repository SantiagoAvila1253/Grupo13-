from core.datos import PRESENTE, AUS_J, AUS_I, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE


def reporte_asistencia_por_estudiante(asistencias, alumnos, legajo):
    alumno = next((a for a in alumnos if a[AL_LEGAJO] == legajo), None)
    if not alumno:
        return f"Alumno {legajo} no encontrado."
    nombre = f"{alumno[AL_APELLIDO]}, {alumno[AL_NOMBRE]}"
    total = 0
    presentes = 0
    for (clase_id, l), estado in asistencias.items():
        if l == legajo:
            total += 1
            if estado == PRESENTE:
                presentes += 1
    if total == 0:
        return f"{nombre} no tiene registros."
    porcentaje = (presentes / total) * 100
    return f"{nombre}: {presentes}/{total} clases ({porcentaje:.2f}%)"


def reporte_asistencia_general(asistencias):
    total = len(asistencias)
    presentes = sum(1 for estado in asistencias.values() if estado == PRESENTE)
    porcentaje = (presentes / total * 100) if total > 0 else 0
    return f"Asistencia global: {presentes}/{total} registros ({porcentaje:.2f}%)"


def reporte_por_clase(asistencias, alumnos, clases, clase_id):
    clase = next((c for c in clases if c[0] == clase_id), None)
    nombre_clase = clase[1] if clase else f"Clase {clase_id}"
    presentes = []
    ausentes = []
    for (cid, legajo), estado in asistencias.items():
        if cid == clase_id:
            alumno = next((a for a in alumnos if a[AL_LEGAJO] == legajo), None)
            if not alumno:
                continue
            nombre = f"{alumno[AL_APELLIDO]}, {alumno[AL_NOMBRE]}"
            if estado == PRESENTE:
                presentes.append(nombre)
            else:
                ausentes.append(nombre)
    if not presentes and not ausentes:
        return f"No hay registros para {nombre_clase}."
    return (
        f"Clase: {nombre_clase}\n"
        f" Presentes ({len(presentes)}): {', '.join(presentes) if presentes else '---'}\n"
        f" Ausentes ({len(ausentes)}): {', '.join(ausentes) if ausentes else '---'}"
    )
