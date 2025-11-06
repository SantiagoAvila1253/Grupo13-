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
"""
import os, json
from core import validadores

def test_docentes_json():
    """
    Objetivo:
    - Validar que registros de docentes en docentes.json:

    Criterios:
    - El archivo no debe estar vacío.
    - Cada registro debe ser un dict y contener las claves "dni" y "clave".
    - dni_valido(dni) debe ser True.
    - password_valida(clave, 4) debe ser True
    """

    # Ruta al JSON de docentes
    ruta = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "docentes.json"))

    # Leer archivo
    with open(ruta, "r", encoding="utf-8") as a:
        docentes = json.load(a)

    # Debe haber al menos un docente
    assert docentes, "El archivo docentes.json está vacío"

    # Recorrido y validaciones
    for id_docente, reg in docentes.items():
        # Tipo del registro
        assert isinstance(reg, dict), f"El registro {id_docente} no es un dict: {type(reg).__name__}"

        # Claves requeridas
        assert "dni" in reg, f"Falta la clave 'dni' en el docente {id_docente}"
        assert "clave" in reg, f"Falta la clave 'clave' en el docente {id_docente}"

        dni = str(reg["dni"]).strip()
        clave = str(reg["clave"])

        # DNI válido
        assert validadores.dni_valido(dni), f"DNI inválido en {id_docente}: {dni!r}"

        # Clave válida
        assert validadores.password_valida(clave, 4), f"Clave inválida en {id_docente}: {clave!r}"
