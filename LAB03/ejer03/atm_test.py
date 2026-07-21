# test_atm.py
import pytest
from atm import ATM, SaldoInsuficienteError, MontoInvalidoError

@pytest.fixture
def mi_cajero():
    """Fixture: proporciona un ATM con S/.1000 de saldo inicial."""
    return ATM(saldo_inicial=1000.0)

# ---Consulta de Saldo ---

def test_saldo_inicial_correcto(mi_cajero):
    """TC-01: Verifica que el saldo inicial sea el esperado."""
    assert mi_cajero.consultar_saldo() == 1000.0

def test_consulta_no_modifica_estado(mi_cajero):
    """TC-12: La consulta de saldo no debe alterar el saldo."""
    mi_cajero.consultar_saldo()
    mi_cajero.consultar_saldo()
    assert mi_cajero.consultar_saldo() == 1000.0

# ---Depósitos ---

def test_deposito_valido(mi_cajero):
    """TC-02: Un depósito positivo debe incrementar el saldo."""
    mi_cajero.depositar(500.0)
    assert mi_cajero.consultar_saldo() == 1500.0

@pytest.mark.parametrize("monto", [-200, 0])
def test_deposito_invalido_lanza_excepcion(mi_cajero, monto):
    """TC-06 y TC-07: Depósitos <= 0 lanzan MontoInvalidoError."""
    with pytest.raises(MontoInvalidoError):
        mi_cajero.depositar(monto)

# --- Retiros ---

def test_retiro_valido(mi_cajero):
    """TC-03: Un retiro válido disminuye el saldo correctamente."""
    mi_cajero.retirar(300.0)
    assert mi_cajero.consultar_saldo() == 700.0

def test_retiro_exacto_al_saldo(mi_cajero):
    """TC-04: Retirar el total disponible deja el saldo en 0."""
    mi_cajero.retirar(1000.0)
    assert mi_cajero.consultar_saldo() == 0.0

def test_retiro_mayor_al_saldo_lanza_excepcion(mi_cajero):
    """TC-05: Retirar más de lo disponible lanza SaldoInsuficienteError."""
    with pytest.raises(SaldoInsuficienteError):
        mi_cajero.retirar(1001.0)

@pytest.mark.parametrize("monto_neg", [-50, 0])
def test_retiro_invalido_lanza_excepcion(mi_cajero, monto_neg):
    """TC-08: Retiros <= 0 lanzan MontoInvalidoError."""
    with pytest.raises(MontoInvalidoError):
        mi_cajero.retirar(monto_neg)

# --- Casos Límite y Secuencias ---

def test_saldo_inicial_negativo_lanza_excepcion():
    """TC-09: No se puede inicializar un ATM con saldo negativo."""
    with pytest.raises(MontoInvalidoError):
        ATM(saldo_inicial=-500)

def test_multiples_depositos_acumulados(mi_cajero):
    """TC-10: Verifica la acumulación de múltiples depósitos."""
    depositos = [100, 200, 300]
    for d in depositos:
        mi_cajero.depositar(d)
    assert mi_cajero.consultar_saldo() == 1600.0

@pytest.mark.parametrize("monto_retiro, saldo_restante", [
    (100.0, 900.0),
    (200.0, 800.0),
    (300.0, 700.0)
])
def test_multiples_retiros_parametrizados(mi_cajero, monto_retiro, saldo_restante):
    """TC-11: Verifica retiros individuales usando parametrize."""
    mi_cajero.retirar(monto_retiro)
    assert abs(mi_cajero.consultar_saldo() - saldo_restante) < 0.001