import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""
Configuración global de pytest:
Asegura que, al ejecutar las pruebas, 
el directorio raíz del proyecto (grupo13) se agregue al sys.path.
De esta forma, los módulos del proyecto pueden importarse 
directamente (por ejemplo, 'from core import validadores')
sin errores de importación.

PASO A PASO PARA EJECUTAR:

DEFAULT:
pytest test_unitarios_asistencia.py

CON PRINTS INDICANDO PASS:
pytest -s tests/test_unitarios_asistencia.py
"""

import os, csv
from core import validadores


def test_asistencia_csv():
    """
    Objetivo:
    - Validar la estructura y contenido básico del archivo asistencia.csv.

    Criterios:
    - El archivo debe existir y no estar vacío.
    - La cabecera debe coincidir exactamente con:
        ["clase_id", "legajo", "apellido", "nombre", "estado"]
    - Debe haber al menos dos registros de datos (además de la cabecera).
    - Cada fila de datos debe cumplir las reglas de validación definidas en core.validadores.
      Consideración: el campo 'estado' puede estar vacío si aún no se tomó asistencia.
    """

    # Ruta al archivo CSV
    ruta = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "data", "asistencia.csv")
    )
    assert os.path.exists(ruta), "El archivo asistencia.csv no existe"
    print("PASS: archivo asistencia.csv encontrado.")

    # Leer contenido del CSV
    with open(ruta, "r", encoding="utf-8") as a:
        lector = csv.reader(a, delimiter=";")
        filas = [fila for fila in lector]

    # Validar que el archivo no esté vacío
    assert filas, "El archivo asistencia.csv está vacío"
    print(f"PASS: archivo leído con {len(filas)} filas (incluyendo cabecera).")

    # Validar cabecera
    assert filas[0] == [
        "clase_id",
        "legajo",
        "apellido",
        "nombre",
        "estado",
    ], f"Cabecera inesperada: {filas[0]}"
    print("PASS: cabecera válida.")

    # Validar que haya al menos dos registros (cabecera + datos)
    assert len(filas) >= 2, "Se esperaban al menos dos filas incluyendo la cabecera"
    print("PASS: contiene al menos una fila de datos.")

    # Validar cada fila de datos según los validadores
    for i, fila in enumerate(filas[1:], start=2):  # Empieza en 2 por la cabecera
        assert len(fila) == 5, f"Fila {i} no tiene 5 columnas: {fila!r}"
        clase_id, legajo, apellido, nombre, estado = fila

        # IDs numéricos
        assert validadores.validar_numero_entero(
            clase_id
        ), f"clase_id inválido en línea {i}: {clase_id!r}"
        assert validadores.validar_numero_entero(
            legajo
        ), f"legajo inválido en línea {i}: {legajo!r}"

        # Apellido / Nombre
        assert validadores.nom_ape_valido(
            apellido
        ), f"Apellido inválido en línea {i}: {apellido!r}"
        assert validadores.nom_ape_valido(
            nombre
        ), f"Nombre inválido en línea {i}: {nombre!r}"

        # Estado: puede ser vacío (no tomada), o válido según regla
        estado_norm = estado.strip().upper()
        if estado_norm:  # solo valida si trae algo
            assert validadores.validar_estado_asistencia(
                estado_norm
            ), f"Estado inválido en línea {i}: {estado!r}"

    print("PASS: todas las filas cumplen con las reglas de validación.")
