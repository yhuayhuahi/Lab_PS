from pares_e_impares import clasificar_paridad

def ejecutar_interfaz():
    try:
        entrada = input("¿Cuántos números deseas ingresar? ")
        cantidad = int(entrada)

        if cantidad < 0:
            print("La cantidad de números no puede ser negativa.")
            return

        numeros = []

        for i in range(cantidad):
            num = int(input(f"Ingrese un número entero: "))
            numeros.append(num)

        print("\n")

        for n in numeros:
            print(f"El {n} es {clasificar_paridad(n)}.")

    except ValueError:
        print(f"Error: El valor ingresado no es un número entero válido.")

if __name__ == "__main__":
    ejecutar_interfaz()