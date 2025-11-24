from core.validadores import dni_valido, validar_cadena_estricta, RE_DNI

print(dni_valido("1234567"))      # True
print(dni_valido("12345678"))     # True
print(dni_valido("abc123"))       # False

try:
    validar_cadena_estricta("123456", RE_DNI, "DNI")
except Exception as e:
    print("Error esperado:", e)
