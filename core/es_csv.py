# Entrada/Salida CSV
"""
- Estructura de cada fila (matriz / lista de listas):
    clase_id;legajo;apellido;nombre;estado

- Criterios:
    * La validación completa de datos (forma y semántica) se hace en los menús/validadores,
      al momento del ingreso de datos por el usuario.
    * Solo dejamos una validación de cantidad de las 5 columnas para evitar corrupción del CSV con advertencia interna (sin ofrecer respaldo).
    * Respaldo (S/N) solo ante errores de E/S (existencia/lectura/escritura).
    * Lectura usando .readline() (iterativa) para buen rendimiento con archivos grandes.
    * Manejo de excepciones detallado, mensajes claros y pausa al finalizar cada acción.
"""

import os
from datetime import datetime

from core.datos import CABECERA_CSV, CSV_SEP
from core.es_json import preguntar_respaldo, pausa

# Rutas
RUTA_ASISTENCIA = "data/asistencia.csv"
CARPETA_RESPALDO = "data/respaldo"


# Genera un nombre único de respaldo preservando la extensión del archivo base (CSV)
def nombre_respaldo_csv(base):
    """
    Ejemplo: asistencia_2025-11-03_22-11-59.csv

        Módulo datetime:
    ----------------
    - datetime.now(): fecha y hora actual del sistema.
    - strftime("%Y-%m-%d_%H-%M-%S"): convierte a texto con ese formato.

    Módulo os:
    ----------
    - os.path.basename(base): extrae el nombre del archivo sin la ruta.
    - os.path.splitext(nombre): separa (nombre_sin_ext, ".ext"), usamos ambos.
    """
    
    marca_temporal = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_base = os.path.basename(base)
    raiz, extension = os.path.splitext(nombre_base)
    return f"{raiz}_{marca_temporal}{extension}"


# Guarda una copia de respaldo del CSV (con o sin contenido, pero siempre con cabecera)
def guardar_respaldo_csv(nombre_archivo_destino, filas=None):
    """
    Si 'filas' es None o lista vacía, se respalda solo la cabecera.
    Si 'filas' tiene contenido (lista de listas), se escribe cabecera + filas.
    """
    try:
        destino = os.path.join(CARPETA_RESPALDO, nombre_respaldo_csv(nombre_archivo_destino))
        with open(destino, "w", encoding="utf-8") as archivo:
            # Cabecera fija
            archivo.write(CSV_SEP.join(CABECERA_CSV) + "\n")
            # Filas (opcional)
            if filas:
                for fila in filas:
                    linea = CSV_SEP.join(str(campo) for campo in fila)
                    archivo.write(linea + "\n")
        print(f"Se guardó una copia de respaldo como {destino}")
    except Exception as error:
        print("No se pudo guardar la copia de respaldo del CSV.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
    finally:
        print("Comunicate con soporte técnico.")
        pausa()
        return


# Validación mínima para evitar corrupción del CSV
def validar_formato_fila(fila):
    """
    - Evita corrupción del CSV (exige exactamente 5 columnas).
    """
    return isinstance(fila, (list, tuple)) and len(fila) == 5


# Lectura del CSV con .readline() (devuelve matriz SIN la cabecera)
def leer_asistencia():
    """
    Manejo de errores:
      - FileNotFoundError, OSError → informa, ofrece respaldo (solo cabecera), devuelve []
    """

    print("Leyendo archivos...")
    matriz = []
    try:
        with open(RUTA_ASISTENCIA, "r", encoding="utf-8") as archivo:
            # 1) Leer primera línea (cabecera)
            cabecera = archivo.readline()
            if not cabecera:
                # Archivo vacío → error, ofrecer respaldo vacío
                print("No se pudo ejecutar la acción. Motivo: el archivo de asistencia está vacío.")
                if preguntar_respaldo():
                    guardar_respaldo_csv(RUTA_ASISTENCIA, [])
                else:
                    print("No se realizó ninguna copia de respaldo.")
                    print("Comunicate con soporte técnico.")
                    pausa()
                return []

            # 2) Leer el resto del archivo línea por línea
            while True:
                linea = archivo.readline()
                if not linea:
                    break  # fin de archivo

                # Eliminamos solo el salto de línea final
                columnas = linea.rstrip("\n").split(CSV_SEP)

                # Si no son 5 columnas, omitimos
                if not validar_formato_fila(columnas):
                    print("Advertencia interna: se omitió una fila con formato inválido (no impacta al usuario).")
                    continue

                matriz.append(columnas)

        return matriz

    except FileNotFoundError as error:
        print(f"No se pudo ejecutar la acción. Motivo: archivo inexistente: {RUTA_ASISTENCIA}.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        if preguntar_respaldo():
            guardar_respaldo_csv(RUTA_ASISTENCIA, [])
        else:
            print("No se realizó ninguna copia de respaldo.")
            print("Comunicate con soporte técnico.")
            pausa()
        return []

    except OSError as error:
        print(f"No se pudo ejecutar la acción. Motivo: error de acceso al archivo {RUTA_ASISTENCIA}.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        if preguntar_respaldo():
            guardar_respaldo_csv(RUTA_ASISTENCIA, [])
        else:
            print("No se realizó ninguna copia de respaldo.")
            print("Comunicate con soporte técnico.")
            pausa()
        return []


# Agrega UNA fila al final (modo append), guard mínimal activo
def agregar_fila_asistencia(fila):

    if not validar_formato_fila(fila):
        print("Error interno: la fila de asistencia debe tener exactamente 5 columnas. Revisá los validadores.")
        return

    try:
        with open(RUTA_ASISTENCIA, "a", encoding="utf-8") as archivo:
            linea = CSV_SEP.join(str(campo) for campo in fila)
            archivo.write(linea + "\n")

        print("La acción se realizó correctamente.")
        pausa()
        return

    except OSError as error:
        print(f"No se pudo ejecutar la acción. Motivo: error al escribir en {RUTA_ASISTENCIA}.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        # En error de E/S sí ofrecemos respaldo (con cabecera + esta fila)
        if preguntar_respaldo():
            guardar_respaldo_csv(RUTA_ASISTENCIA, [fila])
        else:
            print("No se realizó ninguna copia de respaldo.")
            print("Comunicate con soporte técnico.")
            pausa()
        return


# Agrega VARIAS filas al final (modo append), omitiendo inválidas
def agregar_filas_asistencia(filas):

    try:
        with open(RUTA_ASISTENCIA, "a", encoding="utf-8") as archivo:
            for fila in filas:
                if not validar_formato_fila(fila):
                    print("Advertencia interna: se omitió una fila con formato inválido durante el append múltiple.")
                    continue
                linea = CSV_SEP.join(str(campo) for campo in fila)
                archivo.write(linea + "\n")

        print("La acción se realizó correctamente.")
        pausa()
        return

    except OSError as error:
        print(f"No se pudo ejecutar la acción. Motivo: error al escribir en {RUTA_ASISTENCIA}.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        if preguntar_respaldo():
            filas_validas = [f for f in filas if validar_formato_fila(f)]
            guardar_respaldo_csv(RUTA_ASISTENCIA, filas_validas)
        else:
            print("No se realizó ninguna copia de respaldo.")
            print("Comunicate con soporte técnico.")
            pausa()
        return


# Sobrescribe COMPLETAMENTE el CSV con cabecera + matriz (omite inválidas)
def guardar_asistencia_sobrescribir(matriz):

    try:
        with open(RUTA_ASISTENCIA, "w", encoding="utf-8") as archivo:
            # Cabecera fija
            archivo.write(CSV_SEP.join(CABECERA_CSV) + "\n")
            # Filas
            for fila in matriz:
                if not validar_formato_fila(fila):
                    print("Advertencia interna: se omitió una fila por formato inválido durante la escritura total.")
                    continue
                linea = CSV_SEP.join(str(campo) for campo in fila)
                archivo.write(linea + "\n")

        print("La acción se realizó correctamente.")
        pausa()
        return

    except OSError as error:
        print(f"No se pudo ejecutar la acción. Motivo: error al guardar {RUTA_ASISTENCIA}.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        if preguntar_respaldo():
            filas_validas = [f for f in matriz if validar_formato_fila(f)]
            guardar_respaldo_csv(RUTA_ASISTENCIA, filas_validas)
        else:
            print("No se realizó ninguna copia de respaldo.")
            print("Comunicate con soporte técnico.")
            pausa()
        return