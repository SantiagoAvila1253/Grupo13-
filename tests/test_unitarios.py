import os
import json
import csv
from funcionalidades.reportes import reporte_asistencia_general



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