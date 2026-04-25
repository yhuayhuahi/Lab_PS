# Programa para calcular el área de un rectángulo

try:
    base = float(input("Ingresa la base del rectángulo (número entero o decimal): "))
    altura = float(input("Ingresa la altura del rectángulo (número entero o decimal): "))

    # Validar que los valores sean positivos
    if base <= 0 or altura <= 0:
        print("La base y la altura deben ser números positivos.")
    else:
        # Calcular el área
        area = base * altura

        # Mostrar resultados
        print(f"\nBase ingresada: {base}")
        print(f"Altura ingresada: {altura}")
        print(f"Área del rectángulo: {area}")

except ValueError:
    print("Por favor, ingresa solo números válidos (enteros o decimales).")

