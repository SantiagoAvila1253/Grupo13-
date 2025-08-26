# Función Loguin del usuario

def login_usuario(usuarios_docentes, estado):

    # bienvenida y menú inicial
    bienvenida = "Te damos la Bienvenida al sistema de presentismo.\n"
    mostrar_menu_inicio = (
        "Ingresá el número de la opción que querés realizar:\n\n"
        "1- Loguearme al sistema\n"
        "2- Reiniciar la contraseña\n"
        "3- Salir del sistema\n"
    )

    # pedir al usuario una opción del menú
    print(bienvenida)
    print(mostrar_menu_inicio)
    opcion_menu = input("Elegí una opción del menú: ")

    # validar opción ingresada
    while opcion_menu not in ("1", "2", "3"):
        print("El valor ingresado no es válido.\n")
        print(mostrar_menu_inicio)
        opcion_menu = input("Elegí una opción: ")

    # en la opción 1 pedir credenciales del usuario
    if opcion_menu == "1":
        dni = pedir_dni(usuarios_docentes)

    # Si dni no es -1 el usuario sigue en el sistema ???
    if dni != -1:
        # buscamos el usuario en la matriz de usuarios a ver si existe
        idUsuario = buscarUsuario(usuarios, dni)

        # si existe el usuario le pedimos que ingrese su clave o la reinicie
        if idUsuario != -1:
            clave = input(
                "Ingresá tu contraseña (ingresá -1 para reiniciar la contraseña o -2 para salir): "
            )
            while (
                clave != usuarios[idUsuario][0][4] and clave != "-1" and clave != "-2"
            ):
                print("Contraseña incorrecta.")
                clave = input(
                    "Ingresá tu contraseña: "
                )  # tiene intentos infinitos hasta que se rinda o le pegue

            # Si la clave ingresada coincide con la clave guardada en la matriz de usuarios inicia la sesión e ingresa al menú
            if clave == usuarios[idUsuario][0][4]:
                os.system("cls" if os.name == "nt" else "clear")
                # cambia el estado y mantiene al usuario con sesión activa y dentro del sistema hasta que este decida salir
                estado = 2
                print(
                    "Hola",
                    usuarios[idUsuario][0][1],
                    usuarios[idUsuario][0][2],
                    ", iniciaste sesión correctamente.",
                )
                while estado == 2:
                    estado = menuUsuario(usuarios, idUsuario, estado)

            # si ingresa -1 va a la opción de generar una nueva contraseña
            elif clave == "-1":
                nueva = validaContraseña()
                usuarios[idUsuario][0][4] = nueva
                input(
                    "Clave reiniciada. Volvé a iniciar sesión. Apretá Enter para continuar."
                )
                # después de reiniciar sale del sistema y tiene que volver a loguearse
                estado = 1
                print(salir)

            # si ingresa -2 sale del sistema
            else:
                estado = 0
                print(salir)

    # Si el usuario quiere salir, sale del sistema
    else:
        estado = 0
        print(f"{salir}")

    return estado


# función para pedir y validar DNI
# ??? validar con int o string, como se va a hacer el manejo de excepciones para saber qué método elegir
def pedir_dni(usuarios_docentes):
    print("Ingresá tu usuario (DNI)")
    # ingreso a la validación del ingreso del input del usuario en DNI
    dniInvalido = True
    while dniInvalido:
        dni = input(
            "Ingresá tu número de DNI sin puntos, comas ni espacios o -1 para salir: "
        )

        # Validar si el usuario desea salir
        if dni == "-1":
            dni = -1
            dniInvalido = False
        else:
            # Validar que sean solo números
            soloNumeros = True
            i = 0
            largoDni = len(dni)
            while i < largoDni and soloNumeros:
                if dni[i] < "0" or dni[i] > "9":
                    soloNumeros = False
                i += 1

            # Validar cantidad de caracteres
            if soloNumeros:
                if largoDni >= 7 and largoDni <= 8:
                    dniInvalido = False
                    dni = int(dni)
                else:
                    print("Verificá la cantidad de dígitos (7 u 8).")
            else:
                print("Valor inválido, solo se aceptan números.")

    # retorna el valor de dni
    return dni


# __Funciones complementarias__


# Función para busqueda de usuario ingresado en la función loginUsuario a través de la función pedirDni
def buscarUsuario(usuarios, dni):
    i = 0
    pos = -1
    largoUsuarios = len(usuarios)
    while i < largoUsuarios:
        if (
            usuarios[i][0][0] == dni
        ):  # usuarios[i][0] son los datos del usuario, [0] es la pos del dni
            pos = i
        i += 1

    # devuelve la posición o si no lo encuentra retorna -1
    return pos


# Función para solicitar una nueva contraseña y la validarla (mínimo de 4 caracreres)
def validaContraseña():
    caracteresMinimos = 4
    nueva = input("Ingresá tu nueva contraseña (4 caracteres) o -1 para salir: ")
    largoNueva = len(nueva)

    if nueva != "-1":
        while nueva != "-1" and largoNueva < caracteresMinimos:
            nueva = input(
                "Contraseña invalida, debe tener al menos 4 caracteres o -1 para volver al inicio: "
            )
            largoNueva = len(nueva)

    return nueva