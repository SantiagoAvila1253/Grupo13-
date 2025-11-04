# Módulo: Menús del sistema

def mostrar_menu_login():
    print("\n--- LOGIN ---")
    print("1) Ingresar al sistema")
    print("2) Resetear contraseña")
    print("3) Salir")

def mostrar_menu_principal():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1) Gestión de alumnos")
    print("2) Gestión de asistencias")
    print("3) Filtros")
    print("4) Reportes")
    print("9) Cerrar sesión")
    print("0) Salir")

def mostrar_menu_alumnos():
    print("\n--- MENÚ ALUMNOS ---")
    print("1) Listar alumnos")
    print("2) Alta alumno")
    print("3) Baja alumno")
    print("4) Modificar alumno")
    print("9) Cerrar sesión")
    print("0) Volver")

def mostrar_menu_asistencia():
    print("\n--- MENÚ ASISTENCIA ---")
    print("1) Ingresá un ID de clase para cargar asistencia")
    print("2) Modificar registros por clase")
    print("3) Filtrar")
    print("4) Reportes")
    print("9) Cerrar sesión")
    print("0) Volver")

def mostrar_submenu_filtrar():
    print("1) Filtrar por apellido")
    print("2) Filtrar por legajo")
    print("3) Filtrar por estado (Pes; AJ; AI; sin filtro)")
    print("4) Limpiar todos los filtros")
    print("0) Volver")

def mostrar_menu_reportes():
    print("\n--- MENÚ REPORTES ---")
    print("1) Reporte general de asistencia")
    print("2) Presentes por clase")
    print("3) Porcentaje de asistencia por alumno")
    print("9) Cerrar sesión")
    print("0) Volver")