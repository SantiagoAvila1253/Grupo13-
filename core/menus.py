# Módulo: Menús del sistema
from colorama import Fore, Style

def mostrar_menu_login():
    print(Fore.CYAN + Style.BRIGHT + "\n--- LOGIN ---")
    print("1) Ingresar al sistema")
    print("2) Resetear contraseña")
    print(Fore.RED + "3) Salir")

def mostrar_menu_principal():
    print(Fore.CYAN + Style.BRIGHT + "\n--- MENÚ PRINCIPAL ---")
    print("1) Gestión de alumnos")
    print("2) Gestión de asistencias")
    print("3) Filtros")
    print("4) Reportes")
    print(Fore.YELLOW + "9) Cerrar sesión")
    print(Fore.RED + "0) Salir")

def mostrar_menu_alumnos():
    print(Fore.CYAN + Style.BRIGHT + "\n--- MENÚ ALUMNOS ---")
    print("1) Listar alumnos")
    print("2) Alta alumno")
    print(Fore.RED + "3) Baja alumno") 
    print("4) Modificar alumno")
    print(Fore.YELLOW + "9) Cerrar sesión")
    print(Fore.YELLOW + "0) Volver")

def mostrar_menu_asistencia():
    print(Fore.CYAN + Style.BRIGHT + "\n--- MENÚ ASISTENCIA ---")
    print("1) Ingresá un ID de clase para cargar asistencia")
    print("2) Modificar registros por clase")
    print("3) Filtrar")
    print("4) Reportes")
    print(Fore.YELLOW + "9) Cerrar sesión")
    print(Fore.YELLOW + "0) Volver")

def mostrar_menu_filtrar():
    print(Fore.CYAN + Style.BRIGHT + "\n--- MENÚ DE FILTROS ---")
    print("1) Filtrar asistencia por apellido")
    print("2) Filtrar asistencia por legajo")
    print("3) Filtrar asistencia por estado (P, AJ, AI)")
    print("4) Filtrar alumnos por apellido")
    print("5) Filtrar clases por mes (ej. '03' para marzo)")
    print(Fore.YELLOW + "0) Volver")

def mostrar_menu_reportes():
    print(Fore.CYAN + Style.BRIGHT + "\n--- MENÚ REPORTES ---")
    print("1) Reporte general de asistencia")
    print("2) Presentes por clase")
    print("3) Porcentaje de asistencia por alumno")
    print("4) Top 5 alumnos con más inasistencias")
    print(Fore.YELLOW + "9) Cerrar sesión")
    print(Fore.YELLOW + "0) Volver")