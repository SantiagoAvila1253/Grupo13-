import sys
from pathlib import Path

# Agrega la raíz del proyecto al path para permitir los imports de core.*
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from core.validadores import validar_cadena_estricta, dni_valido, RE_DNI


"""
TESTS SOBRE LA VALIDACIÓN DE DNI
Incluye:
 - validar_cadena_estricta (función estricta → usa raises)
 - dni_valido (función funcional → retorna True/False)

 PASO A PASO PARA EJECUTAR:

DEFAULT:
pytest tests/test_unitarios_funciones_dni.py -vv

CON PRINTS INDICANDO PASS:
pytest -s tests/test_unitarios_funciones_dni.py
 """


# Casos válidos: deben pasar la validación estricta y limpiar espacios.
@pytest.mark.parametrize(
    "entrada, salida_esperada",
    [
        ("1234567", "1234567"),          # 7 dígitos
        ("12345678", "12345678"),        # 8 dígitos
        ("   87654321   ", "87654321"),  # sin espacios
    ]
)
def test_validar_cadena_estricta_dni_valido(entrada, salida_esperada):
    resultado = validar_cadena_estricta(entrada, RE_DNI, "DNI")
    assert resultado == salida_esperada


# Casos inválidos por contenido, deben generar ValueError.

@pytest.mark.parametrize(
    "entrada, mensaje_parcial",
    [
        ("", "no puede estar vacío"),
        ("   ", "no puede estar vacío"),
        ("abc123", "7 u 8 dígitos"),
        ("123456", "7 u 8 dígitos"),
        ("123456789", "7 u 8 dígitos"),
    ]
)
def test_validar_cadena_estricta_dni_value_error(entrada, mensaje_parcial):
    with pytest.raises(ValueError) as excinfo:
        validar_cadena_estricta(entrada, RE_DNI, "DNI")

    assert mensaje_parcial.lower() in str(excinfo.value).lower()


# Casos inválidos por tipo, deben generar TypeError.
# Se verifica el tipo recibido en el mensaje y la indicación de soporte.
@pytest.mark.parametrize(
    "entrada, tipo_esperado",
    [
        (None, "NoneType"),
        (12345678, "int"),
        ([], "list"),
        ({}, "dict"),
    ]
)
def test_validar_cadena_estricta_dni_type_error(entrada, tipo_esperado):
    with pytest.raises(TypeError) as excinfo:
        validar_cadena_estricta(entrada, RE_DNI, "DNI")

    mensaje = str(excinfo.value)
    assert tipo_esperado in mensaje
    assert "contacte al soporte técnico" in mensaje.lower()


# TESTS SOBRE dni_valido. No usa raises. Retorna True/False.
# Casos válidos: deben devolver True.
@pytest.mark.parametrize(
    "entrada",
    [
        "1234567",
        "12345678",
        "   23456789   ",
    ]
)
def test_dni_valido_true(entrada):
    assert dni_valido(entrada) is True


# Casos inválidos por contenido: deben devolver False.
@pytest.mark.parametrize(
    "entrada",
    [
        "abc123",
        "123456",       # 6 dígitos
        "123456789",    # 9 dígitos
        "",
        "   ",
    ]
)
def test_dni_valido_false(entrada):
    assert dni_valido(entrada) is False


# Casos inválidos por tipo: deben devolver False.
@pytest.mark.parametrize(
    "entrada",
    [
        None,
        12345678,
        [],
        {},
    ]
)
def test_dni_valido_tipo_invalido(entrada):
    assert dni_valido(entrada) is False
