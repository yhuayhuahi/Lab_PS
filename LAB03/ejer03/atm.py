# atm.py

class SaldoInsuficienteError(Exception):
    """Se lanza cuando el retiro excede el saldo disponible."""
    pass

class MontoInvalidoError(Exception):
    """Se lanza cuando el monto es cero o negativo."""
    pass

class ATM:
    def __init__(self, saldo_inicial: float = 1000.0):

        if saldo_inicial < 0:
            raise MontoInvalidoError("El saldo inicial no puede ser.")
        self._saldo = saldo_inicial

    def consultar_saldo(self) -> float:
        """Retorna el saldo actual sin modificar el estado."""
        return self._saldo

    def depositar(self, monto: float) -> None:

        if monto <= 0:
            raise MontoInvalidoError(f"Monto inválido: {monto}. Debe ser positivo.")
        self._saldo += monto

    def retirar(self, monto: float) -> None:

        if monto <= 0:
            raise MontoInvalidoError(f"Monto inválido: {monto}. Debe ser positivo.")
        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente: tiene S/.{self._saldo}, intenta retirar S/.{monto}"
            )
        self._saldo -= monto