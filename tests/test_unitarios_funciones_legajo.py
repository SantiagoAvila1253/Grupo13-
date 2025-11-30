import sys
from pathlib import Path

# Agrega la raíz del proyecto al path para permitir los imports de core.*
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from core.validadores import validar_legajo_existente


"""
TESTS SOBRE LA VALIDACIÓN DE LEGAJO
Incluye:
 - validar_legajo_existente (valida formato + existencia en el diccionario de alumnos)

PASO A PASO PARA EJECUTAR:

DEFAULT (detalle de cada test):
    pytest tests/test_unitarios_funciones_legajo.py -vv

CON PRINTS (si agrego prints de depuración):
    pytest -s tests/test_unitarios_funciones_legajo.py
"""


# Diccionario de alumnos de prueba (mock). Claves string, como en alumnos.json.
ALUMNOS_MOCK = {
    "1": {"nombre": "Ana"},
    "2": {"nombre": "Bruno"},
    "10": {"nombre": "Carla"},
}


# Casos válidos: legajo con formato válido y existente en el diccionario. Debe devolver True.
@pytest.mark.parametrize(
    "legajo",
    [
        "1",          # existe
        "2",          # existe
        "10",       # existe
    ]
)
def test_validar_legajo_existente_true(legajo):
    assert validar_legajo_existente(legajo, ALUMNOS_MOCK) is True


# Casos con formato válido pero legajo inexistente. Debe devolver False.
@pytest.mark.parametrize(
    "legajo",
    [
        "3",      # no está en el dict
        "99",     # no está en el dict
    ]
)
def test_validar_legajo_existente_false_inexistente(legajo):
    assert validar_legajo_existente(legajo, ALUMNOS_MOCK) is False


# Casos con formato inválido (no numérico, vacío, <= 0). Suponemos que validar_legajo_formato devuelve False y entonces validar_legajo_existente también devuelve False sin levantar errores
@pytest.mark.parametrize(
    "legajo",
    [
        "0",       # no positivo
        "-1",      # negativo
        "",        # vacío
        "   ",     # espacios
        "abc",     # no numérico
    ]
)
def test_validar_legajo_existente_false_formato_invalido(legajo):
    assert validar_legajo_existente(legajo, ALUMNOS_MOCK) is False


# Casos con tipo inválido para alumnos_json. Si el legajo tiene formato válido, pero alumnos_json no es dict, debe levantar TypeError con el mensaje correspondiente.
@pytest.mark.parametrize(
    "alumnos_invalido",
    [
        None,
        [],
        "no es un dict",
        123,
    ]
)
def test_validar_legajo_existente_type_error_alumnos(alumnos_invalido):
    # Usamos un legajo válido para asegurarnos de llegar a la validación del tipo.
    legajo_valido = "1"

    with pytest.raises(TypeError) as exinfo:
        validar_legajo_existente(legajo_valido, alumnos_invalido)

    mensaje = str(exinfo.value)
    assert "alumnos_json debe ser un diccionario" in mensaje
