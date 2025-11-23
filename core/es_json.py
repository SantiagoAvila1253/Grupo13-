# Entrada/Salida JSON
"""
Este módulo centraliza la lectura y escritura de las entidades en JSON.

- Estructura por archivo: diccionario de diccionarios (clave externa = ID como string)
- Archivos persistentes:
    + data/alumnos.json
    + data/clases.json
    + data/docentes.json
- Manejo de errores:
    * Se informa el tipo de error y el mensaje
    * Ante error, se consulta si querés guardar una copia de respaldo (S/N)
    * La copia se guarda en data/respaldo/<nombre>_YYYY-MM-DD_HH-MM-SS.json
- No se crean carpetas nuevas ni archivos temporales (.tmp)
- Rutas relativas simples
"""

import os
import json
from datetime import datetime

# Rutas relativas
RUTA_ALUMNOS = "data/alumnos.json"
RUTA_CLASES = "data/clases.json"
RUTA_DOCENTES = "data/docentes.json"
CARPETA_RESPALDO = "data/respaldo"


# Devuelve True si 'obj' es un dict y todos sus valores son dict
def es_diccionario_de_diccionarios(obj):
    if not isinstance(obj, dict):
        return False
    return all(isinstance(v, dict) for v in obj.values())


# Pausa de pantalla para continuar con Enter
def pausa():
    input("(Presioná Enter para continuar)")
    return


# Pregunta si querés guardar una copia de respaldo
def preguntar_respaldo():
    opciones = {"s", "n"}
    while True:
        respuesta = (
            input("¿Querés guardar una copia de respaldo? (S/N): ").strip().lower()
        )
        if respuesta in opciones:
            return respuesta == "s"
        print("Opción inválida. Ingresá 'S' o 'N'.")


# Genera un nombre único para el archivo de respaldo
def nombre_respaldo(base):
    """
    Módulo datetime:
    ----------------
    - Permite trabajar con fechas y horas del sistema.
    - datetime.now() obtiene la fecha y hora actual.
    - strftime("%Y-%m-%d_%H-%M-%S") convierte esa fecha y hora
      en una cadena de texto con el formato deseado:
        %Y → año (ej: 2025)
        %m → mes (ej: 11)
        %d → día (ej: 01)
        %H → hora (00 a 23)
        %M → minutos (00 a 59)
        %S → segundos (00 a 59)
      Los guiones y guion bajo son separadores personalizados.
    """
    marca_temporal = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    """
    Módulo os:
    ----------
    - Proporciona funciones para trabajar con nombres de archivos y rutas.
    - os.path.basename(base): obtiene solo el nombre del archivo,
      quitando la ruta completa. Ejemplo:
        os.path.basename("data/alumnos.json") → "alumnos.json"
    - os.path.splitext(nombre): separa el nombre y la extensión,
      devolviendo una tupla. Ejemplo:
        os.path.splitext("alumnos.json") → ("alumnos", ".json")
    - [0] accede al primer elemento de la tupla, es decir,
      el nombre sin la extensión.
    """
    base_sin_ext = os.path.splitext(os.path.basename(base))[0]

    # Se construye el nuevo nombre del archivo con el formato:
    # nombre_base + "_" + fecha-hora + ".json"
    return f"{base_sin_ext}_{marca_temporal}.json"


# Guarda una copia de respaldo en data/respaldo/ de lo trabajado con nombre único cuando hay un error en el archivo
def guardar_respaldo(nombre_archivo_destino, datos=None):
    """
    Comportamiento
    - Si 'datos' es None → guarda un JSON vacío.
    - Retorna la ruta del respaldo si todo salió bien, o None si falla.
    """
    try:
        os.makedirs(CARPETA_RESPALDO, exist_ok=True)

        # Ruta final del respaldo: data/respaldo/<base>_YYYY-MM-DD_HH-MM-SS.json
        destino = os.path.join(
            CARPETA_RESPALDO, nombre_respaldo(nombre_archivo_destino)
        )

        # Si 'datos' es None => {}, si no => convertimos claves externas a str
        contenido = (
            {}
            if datos is None
            else {str(clave): valor for clave, valor in datos.items()}
        )

        # Escritura del JSON
        with open(destino, "w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=2, sort_keys=True)

        print(f"Se guardó una copia de respaldo como {destino}")
        print("Comunicate con soporte técnico.")
        pausa()
        return destino

    except Exception as error:
        print("No se pudo guardar la copia de respaldo.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        print("Comunicate con soporte técnico.")
        pausa()
        return None


# Lectura general de archivos JSON
def leer_json(ruta):
    """
    Manejo de errores:
      - FileNotFoundError: informar, ofrecer respaldo (vacío), devolver {}
      - JSONDecodeError (archivo corrupto): informar, ofrecer respaldo (vacío), devolver {}
      - OSError: informar, ofrecer respaldo (vacío), devolver {}
    En caso de éxito, confirma la acción.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

            # Verifica que 'datos' sea un diccionario de diccionarios
            if not es_diccionario_de_diccionarios(datos):
                print(
                    f"No se pudo ejecutar la acción. Motivo: estructura inválida en {ruta} (se esperaba un diccionario de diccionarios)."
                )
                print("Comunicate con soporte técnico.")
                pausa()
                return {}

        return datos

    except FileNotFoundError as error:
        print(f"No se pudo ejecutar la acción. Motivo: archivo inexistente: {ruta}.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        print("Comunicate con soporte técnico.")
        pausa()
        return {}

    except json.JSONDecodeError as error:
        print(f"No se pudo ejecutar la acción. Motivo: JSON inválido en {ruta}.")
        # __name__ devuelve el nombre del tipo de error (por ejemplo "JSONDecodeError")
        # lineno y colno indican la línea y columna del archivo donde ocurrió el error JSON
        print(
            f"Tipo de error: {type(error).__name__}. Detalle: línea {error.lineno}, columna {error.colno}."
        )
        print("Comunicate con soporte técnico.")
        pausa()
        return {}

    except OSError as error:
        print(
            f"No se pudo ejecutar la acción. Motivo: error de acceso al archivo {ruta}."
        )
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        print("Comunicate con soporte técnico.")
        pausa()
        return {}


# Guardado general de archivos JSON
def guardar_json(ruta, datos):
    """
    Comportamiento:
    - En éxito: guarda y retorna
    - En error: muestra detalles, ofrece respaldo y pausa.
    - ValueError si 'datos' no es dict válido.
    - OSError si hay error al abrir/escribir.
    """

    # Validación de estructura
    if not es_diccionario_de_diccionarios(datos):
        print(
            "No se pudo ejecutar la acción. Motivo: los valores del diccionario deben ser diccionarios (forma entidad)."
        )
        print("Tipo de error: ValueError.")
        if preguntar_respaldo():
            guardar_respaldo(ruta, None)
            print("Se guardó una copia de respaldo. Comunicate con soporte técnico.")
        else:
            print("No se realizó ninguna copia de respaldo.")
            print("Comunicate con soporte técnico.")
        pausa()
        return

    try:
        # Convierte las claves a string por compatibilidad JSON
        datos_convertidos = {str(clave): valor for clave, valor in datos.items()}

        # Guarda el archivo sobrescribiendo el anterior
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                datos_convertidos, archivo, ensure_ascii=False, indent=2, sort_keys=True
            )

        return  # éxito: sin prints ni pausas

    except OSError as error:
        print(f"No se pudo ejecutar la acción. Motivo: error al guardar {ruta}.")
        print(f"Tipo de error: {type(error).__name__}. Detalle: {error}")
        if preguntar_respaldo():
            guardar_respaldo(ruta, datos)
            print("Se guardó una copia de respaldo. Comunicate con soporte técnico.")
        else:
            print("No se realizó ninguna copia de respaldo.")
            print("Comunicate con soporte técnico.")
        pausa()
        return


# Funciones por entidad
def leer_alumnos():
    """Devuelve el diccionario de alumnos (diccionario de diccionarios)."""
    return leer_json(RUTA_ALUMNOS)


def guardar_alumnos(alumnos):
    """Guarda el diccionario de alumnos (diccionario de diccionarios)."""
    guardar_json(RUTA_ALUMNOS, alumnos)
    return


def leer_clases():
    """Devuelve el diccionario de clases (diccionario de diccionarios)."""
    return leer_json(RUTA_CLASES)


def leer_docentes():
    """Devuelve el diccionario de docentes (diccionario de diccionarios)."""
    return leer_json(RUTA_DOCENTES)


def guardar_docentes(docentes):
    """Guarda el diccionario de docentes (diccionario de diccionarios)."""
    guardar_json(RUTA_DOCENTES, docentes)
    return
