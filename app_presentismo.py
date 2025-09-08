from core import (
    mostrar_menu_principal, mostrar_menu_alumnos, mostrar_menu_asistencia,
    opcion_valida_menu, alumnos, AL_LEGAJO, AL_APELLIDO, AL_NOMBRE, AL_EMAIL
)
from login import login_usuario

def listar_alumnos():
    if not alumnos:
        print("Sin alumnos."); return
    print("\nLEGAJO | APELLIDO, NOMBRE | EMAIL")
    for a in alumnos:
        print(f"{a[AL_LEGAJO]} | {a[AL_APELLIDO]}, {a[AL_NOMBRE]} | {a[AL_EMAIL]}")

def main():
    user = login_usuario()
    if not user:
        print("Salida."); return

    while True:
        mostrar_menu_principal()
        op = input("Elegí una opción: ").strip()
        if not opcion_valida_menu(op, {"0","1","2","3"}):
            print("Opción inválida."); continue

        if op == "0":
            print("Fin."); break

        elif op == "1":
            while True:
                mostrar_menu_alumnos()
                aop = input("Elegí: ").strip()
                if not opcion_valida_menu(aop, {"0","1","2","3","4"}):
                    print("Opción inválida."); continue
                if aop == "0": break
                elif aop == "1": listar_alumnos()
                elif aop == "2": print("Alta (pendiente)")
                elif aop == "3": print("Baja lógica (pendiente)")
                elif aop == "4": print("Modificar (pendiente)")

        elif op == "2":
            mostrar_menu_asistencia()
            sop = input("Elegí: ").strip()
            # ... registrar/consultar (pendiente)

        elif op == "3":
            print("Reportes (pendiente)")

if __name__ == "__main__":
    main()
