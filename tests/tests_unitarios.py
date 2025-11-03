import os
import json
import pytest 

def test_docente_10000_credenciales():
    ruta = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "docentes.json"))
    with open(ruta, "r", encoding="utf-8") as f:
        docentes = json.load(f)

    reg = docentes.get("10000")
    assert reg is not None
    assert reg.get("dni/usuario") == "12345678"
    assert reg.get("clave") == "Clave.123"