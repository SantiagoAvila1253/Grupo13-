from core.datos import PRESENTE, AUS_J, AUS_I, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE


def reporte_asistencia_por_estudiante(asistencias, alumnos, legajo):
    alumno = None
    for a in alumnos:
        if a[AL_LEGAJO] == legajo:
            alumno = a
    if not alumno:
        return f"Alumno {legajo} no encontrado."
    nombre = f"{alumno[AL_APELLIDO]}, {alumno[AL_NOMBRE]}"
    total = 0
    presentes = 0
    for clave in asistencias:
        clase_id, l = clave
        estado = asistencias[clave]
        if l == legajo:
            total += 1
            if estado == PRESENTE:
                presentes += 1
    if total == 0:
        return f"{nombre} no tiene registros."
    porcentaje = (presentes / total) * 100
    return f"{nombre}: {presentes}/{total} clases ({porcentaje:.2f}%)"


def reporte_asistencia_general(asistencias):
    total = 0
    presentes = 0
    for clave in asistencias:
        estado = asistencias[clave]
        total += 1
        if estado == PRESENTE:
            presentes += 1
    porcentaje = (presentes / total * 100) if total > 0 else 0
    return f"Asistencia global: {presentes}/{total} registros ({porcentaje:.2f}%)"

def reporte_asistencia_por_alumnos(asistencias, alumnos):
    reportes = []
    for alumno in alumnos:
        legajo = alumno[AL_LEGAJO]
        reporte = reporte_asistencia_por_estudiante(asistencias, alumnos, legajo)
        reportes.append(reporte)
    return "\n".join(reportes)

def reporte_por_clase(asistencias, alumnos, clases, clase_id):
    nombre_clase = f"Clase {clase_id}"
    fecha = ""
    horario = ""
    for c in clases:
        if c[0] == clase_id:
            nombre_clase = c[1]
            fecha = c[2]
            horario = c[4]
    presentes = []
    ausentes = []
    for clave in asistencias:
        cid, legajo = clave
        estado = asistencias[clave]
        if cid == clase_id:
            alumno = None
            for a in alumnos:
                if a[AL_LEGAJO] == legajo:
                    alumno = a
            if alumno:
                nombre = f"{alumno[AL_APELLIDO]}, {alumno[AL_NOMBRE]}"
                if estado == PRESENTE:
                    presentes.append(nombre)
                else:
                    ausentes.append(nombre)
    if len(presentes) == 0 and len(ausentes) == 0:
        return f"No hay registros para {nombre_clase} en la fecha {fecha}, {horario}."
    resultado = f"Clase: {nombre_clase} | Fecha: {fecha} | Horario: {horario}\n"
    resultado += f" Presentes ({len(presentes)}):\n"
    if presentes:
        for p in presentes:
            resultado += f"   - {p}\n"
    else:
        resultado += "   ---\n"
    resultado += f" Ausentes ({len(ausentes)}):\n"
    if ausentes:
        for a in ausentes:
            resultado += f"   - {a}\n"
    else:
        resultado += "   ---\n"
    return resultado
