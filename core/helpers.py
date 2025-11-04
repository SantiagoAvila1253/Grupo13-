# core/helpers.py

# Funciones de ayuda integradas al modelo nuevo de persistencia contra los JSON (core.es_json)

from core import validadores as val
from core.es_json import leer_alumnos, leer_clases


def pedir_legajo_existente(etiqueta="Legajo"):
    """
    Pide un legajo por input hasta que:
        - sea entero positivo
        - exista como clave en data/alumnos.json
    Devuelve el legajo como int.
    """
    alumnos = leer_alumnos()  # diccionario de diccionarios
    while True:
        texto = input(f"{etiqueta}: ").strip()
        if not val.validar_numero_entero(texto):
            print(f"{etiqueta} inválido: debe ser un entero.")
            continue
        if not val.validar_legajo_formato(texto):
            print(f"{etiqueta} inválido: debe ser mayor que 0.")
            continue
        if not val.validar_legajo_existente(texto, alumnos):
            print(f"{etiqueta} inexistente: {texto}")
            continue
        return int(texto)


def pedir_id_clase_existente(etiqueta="ID de clase"):
    """
    Pide un id de clase por input hasta que:
        - sea entero positivo
        - exista como clave en data/clases.json
    Devuelve el id de clase como int.
    """
    clases = leer_clases()
    while True:
        texto = input(f"{etiqueta}: ").strip()
        if not val.validar_numero_entero(texto):
            print(f"{etiqueta} inválido: debe ser un entero.")
            continue
        if not val.validar_id_clase_formato(texto):
            print(f"{etiqueta} inválido: debe ser mayor que 0.")
            continue
        if not val.validar_id_clase_existente(texto, clases):
            print(f"{etiqueta} inexistente: {texto}")
            continue
        return int(texto)