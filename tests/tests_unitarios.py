import os
import json
import csv
from funcionalidades.reportes import reporte_asistencia_general

def test_docente_credenciales():
    ruta = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "docentes.json"))
    with open(ruta, "r", encoding="utf-8") as a:
        docentes = json.load(a)

    reg = docentes.get("10000")
    assert reg is not None
    assert reg.get("dni/usuario") == "12345678"
    assert reg.get("clave") == "Clave.123"


def test_asistencia_csv():
    ruta = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "asistencia.csv"))
    with open(ruta, "r", encoding="utf-8") as a:
        lector = csv.reader(a, delimiter=';')
        filas = [fila for fila in lector]

    # verificar cabecera
    assert filas[0] == ["clase_id", "legajo", "apellido", "nombre", "estado"]
    # verificar que hay al menos dos registros y que la primera fila de datos coincide
    assert len(filas) >= 3
    assert filas[1] == ["20001", "30001", "Saltid", "Juan", "P"]

def test_reporte_asistencia_general_count_and_percentage():
    asistencias = {
        (1, 100): "P",
        (1, 101): "A",
        (2, 100): "P",
    }
    out = reporte_asistencia_general(asistencias)
    assert out == "Asistencia global: 2/3 registros (66.67%)"

def test_reporte_asistencia_general_empty():
    out = reporte_asistencia_general({})
    assert out == "Asistencia global: 0/0 registros (0.00%)"