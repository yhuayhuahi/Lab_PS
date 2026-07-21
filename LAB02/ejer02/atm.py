# atm.py
# Mini Simulador de Cajero Automático (ATM)
# Pruebas de Software - LAB_01

class ATM:
    """
    Clase que representa un cajero automático con operaciones básicas.
    Saldo inicial: S/.1,000.00
    """

    def __init__(self, saldo_inicial=1000.0):
        self._saldo = saldo_inicial

    def consultar_saldo(self):
        """Retorna el saldo actual."""
        return self._saldo

    def depositar(self, monto):
        """
        Deposita un monto al saldo actual.
        Retorna (True, mensaje) si es exitoso, (False, mensaje) si no.
        """
        if monto <= 0:
            return False, "Monto inválido: el depósito debe ser un valor positivo."
        self._saldo += monto
        return True, f"Depósito exitoso. Nuevo saldo: S/.{self._saldo:.2f}"

    def retirar(self, monto):
        """
        Retira un monto del saldo actual.
        Retorna (True, mensaje) si es exitoso, (False, mensaje) si no.
        """
        if monto <= 0:
            return False, "Monto inválido: el retiro debe ser un valor positivo."
        if monto > self._saldo:
            return False, "Fondos insuficientes: el monto excede el saldo disponible."
        self._saldo -= monto
        return True, f"Retiro exitoso. Nuevo saldo: S/.{self._saldo:.2f}"


def main():
    atm = ATM(saldo_inicial=1000.0)

    while True:
        print("\n" + "=" * 45)
        print(f"   Saldo disponible: S/.{atm.consultar_saldo():.2f}")
        print("=" * 45)
        print("   MENÚ PRINCIPAL")
        print("   1. Consultar Saldo")
        print("   2. Depositar Dinero")
        print("   3. Retirar Dinero")
        print("   4. Salir")
        print("=" * 45)

        opcion = input("   Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            print(f"\n   Saldo actual: S/.{atm.consultar_saldo():.2f}")

        elif opcion == "2":
            try:
                monto = float(input("   Ingrese el monto a depositar: S/."))
                exito, mensaje = atm.depositar(monto)
                print(f"\n   {mensaje}")
            except ValueError:
                print("\n   Error: ingrese un valor numérico válido.")

        elif opcion == "3":
            try:
                monto = float(input("   Ingrese el monto a retirar: S/."))
                exito, mensaje = atm.retirar(monto)
                print(f"\n   {mensaje}")
            except ValueError:
                print("\n   Error: ingrese un valor numérico válido.")

        elif opcion == "4":
            print("\n   Gracias por usar el ATM. ¡Hasta luego!")
            break

        else:
            print("\n   Opción inválida. Seleccione una opción entre 1 y 4.")


if __name__ == "__main__":
    main()


