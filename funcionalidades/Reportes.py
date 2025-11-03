# Reportes de asistencia:
# - Por estudiante
# - Global
# - Por todos los alumnos (batch)
# - Por clase
# - Menú de reportes (loop interactivo)

from core import (
    # Datos
    asistencias, alumnos, clases, PRESENTE, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, CL_ID, CL_MATERIA, CL_FECHA, CL_HORARIO,
    # Menú
    mostrar_menu_reportes,
    # Validadores
    opcion_valida_menu
)

# Resumen de asistencia del alumno: legajo, apellido, nombre. P/T clases (XX.XX%)'
def reporte_asistencia_por_estudiante(asistencias, alumnos, legajo):
    # Buscar alumno por legajo
    alumno = None
    for a in alumnos:
        if a[AL_LEGAJO] == legajo:
            alumno = a  # último match, asumiendo legajos únicos
    if not alumno:
        return f"Alumno {legajo} no encontrado."
    nombre = f"{alumno[AL_APELLIDO]}, {alumno[AL_NOMBRE]}"
    # Contadores
    total = 0
    presentes = 0
    # Recorrer asistencias y acumular solo las del legajo dado
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

# Devuelve 'Asistencia global: P/T registros (XX.XX%)'
def reporte_asistencia_general(asistencias):
    total = 0
    presentes = 0
    # Recorre todos los valores (estados) del diccionario
    for clave in asistencias:
        estado = asistencias[clave]
        total += 1
        if estado == PRESENTE:
            presentes += 1
    porcentaje = (presentes / total * 100) if total > 0 else 0
    return f"Asistencia global: {presentes}/{total} registros ({porcentaje:.2f}%)"

# Reporte por estudiante Si no hay alumnos, devuelve cadena vacía
def reporte_asistencia_por_alumnos(asistencias, alumnos):
    reportes = []
    for alumno in alumnos:
        legajo = alumno[AL_LEGAJO]
        reporte = reporte_asistencia_por_estudiante(asistencias, alumnos, legajo)
        reportes.append(reporte)
    return "\n".join(reportes)

# Resumen textual de la clase Materia, Fecha, Horario, Presentes y Ausentes (por 'Apellido, Nombre')
def reporte_por_clase(asistencias, alumnos, clases, clase_id):
     # Buscar datos de la clase
    nombre_clase = f"Clase {clase_id}"
    fecha = ""
    horario = ""
    for c in clases:
        if c[CL_ID] == clase_id:
            nombre_clase = c[CL_MATERIA]
            fecha = c[CL_FECHA]
            horario = c[CL_HORARIO]
    # Armar listas de nombres según estado
    presentes = []
    ausentes = []
    for clave in asistencias:
        cid, legajo = clave
        estado = asistencias[clave]
        if cid == clase_id:
            # Buscar alumno por legajo (sin break)
            alumno = None
            for a in alumnos:
                if a[AL_LEGAJO] == legajo:
                    alumno = a  # último match
            if alumno:
                nombre = f"{alumno[AL_APELLIDO]}, {alumno[AL_NOMBRE]}"
                if estado == PRESENTE:
                    presentes.append(nombre)
                else:
                    ausentes.append(nombre)
    # Si no hay ninguna marca para esa clase
    if len(presentes) == 0 and len(ausentes) == 0:
        return f"No hay registros para {nombre_clase} en la fecha {fecha}, {horario}."
    # Construcción de la salida
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

def reporte_top_inasistencias(alumnos):
    # Ordenamos por inasistencias (de mayor a menor)
    alumnos_ordenados = sorted(alumnos, key=lambda x: x[3], reverse=True)

    # Aplicamos slicing para obtener los 5 primeros
    top_5 = alumnos_ordenados[0:5:1]  # [inicio:fin:paso]

    print("\n📋 Reporte: 5 alumnos con más inasistencias\n")
    for legajo, apellido, nombre, inasistencias in top_5:
        print(f"{legajo} - {apellido}, {nombre}: {inasistencias} inasistencias")

# Loop del submenú de reportes.
def menu_reportes():
    en_reportes = True
    while en_reportes:
        mostrar_menu_reportes()
        opcion = input("Elegí una opción: ").strip()
        if not opcion_valida_menu(opcion, {"0", "1", "2", "3", "9"}):
            print("Opción inválida.")
        elif opcion == "0":
            en_reportes = False
        elif opcion == "9":
            return "logout"
        elif opcion == "1":
            print(reporte_asistencia_general(asistencias))
        elif opcion == "2":
            for clase in clases:
                clase_id = clase[CL_ID]
                print(reporte_por_clase(asistencias, alumnos, clases, clase_id))
                print()
        elif opcion == "3":
            for alumno in alumnos:
                print(reporte_asistencia_por_estudiante(asistencias, alumnos, alumno[AL_LEGAJO]))
        elif opcion == "4":
            reporte_top_inasistencias(alumnos)  
    return "volver"
