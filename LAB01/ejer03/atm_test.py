# atm_test.py
# Archivo de pruebas automatizadas para el programa ATM
# Pruebas de Software - LAB_01
#
# Propósito: Verificar automáticamente que atm.py cumple los casos de prueba diseñados.
# Ejecución:  python atm_test.py

from atm import ATM
import random


# Semilla fija para generar montos reproducibles en casos no límite.
RNG = random.Random(20230485)
DEPOSITO_VALIDO = RNG.randint(120, 700)
RETIRO_VALIDO = RNG.randint(120, 500)
DEPOSITO_NEGATIVO = -RNG.randint(50, 300)
RETIRO_NEGATIVO = -RNG.randint(50, 300)
SEQ_DEP_1 = RNG.randint(100, 500)
SEQ_RET_1 = RNG.randint(50, 250)
SEQ_DEP_2 = RNG.randint(50, 300)
SEQ_RET_2 = RNG.randint(50, 250)
POST_INVALIDO_DEPOSITO = RNG.randint(100, 400)

# ─────────────────────────────────────────────
#  Motor de reporte de pruebas
# ─────────────────────────────────────────────
resultados = []

def caso(id_caso, descripcion, obtenido, esperado):
    """Compara obtenido vs esperado y registra el resultado."""
    paso = obtenido == esperado
    estado = "PASÓ  ✅" if paso else "FALLÓ ❌"
    resultados.append((id_caso, descripcion, estado))
    print(f"  [{estado}]  {id_caso} - {descripcion}")
    if not paso:
        print(f"             Esperado : {esperado}")
        print(f"             Obtenido : {obtenido}")


# ─────────────────────────────────────────────
#  GRUPO 1 — Consulta de saldo
# ─────────────────────────────────────────────

def test_saldo_inicial():
    """CP-01: El saldo inicial debe ser exactamente S/.1000.00"""
    atm = ATM()
    caso("CP-01", "Saldo inicial = S/.1000.00", atm.consultar_saldo(), 1000.0)


# ─────────────────────────────────────────────
#  GRUPO 2 — Depósito de dinero
# ─────────────────────────────────────────────

def test_deposito_positivo_actualiza_saldo():
    """CP-02: Depositar un monto positivo incrementa el saldo correctamente."""
    atm = ATM()
    atm.depositar(DEPOSITO_VALIDO)
    esperado = 1000.0 + DEPOSITO_VALIDO
    caso("CP-02", f"Depósito de S/.{DEPOSITO_VALIDO} → saldo = S/.{esperado:.2f}", atm.consultar_saldo(), esperado)

def test_deposito_cero_rechazado():
    """CP-03: Depositar cero debe ser rechazado (monto no positivo)."""
    atm = ATM()
    exito, _ = atm.depositar(0)
    caso("CP-03", "Depósito de S/.0 es rechazado (éxito=False)", exito, False)

def test_deposito_negativo_rechazado():
    """CP-04: Depositar un monto negativo debe ser rechazado."""
    atm = ATM()
    exito, _ = atm.depositar(DEPOSITO_NEGATIVO)
    caso("CP-04", f"Depósito de S/.{DEPOSITO_NEGATIVO} es rechazado (éxito=False)", exito, False)

def test_saldo_sin_cambio_tras_deposito_invalido():
    """CP-05: El saldo no debe cambiar si el depósito es inválido (monto=0)."""
    atm = ATM()
    atm.depositar(0)
    caso("CP-05", "Saldo inalterado tras depósito inválido (0)", atm.consultar_saldo(), 1000.0)


# ─────────────────────────────────────────────
#  GRUPO 3 — Retiro de dinero
# ─────────────────────────────────────────────

def test_retiro_valido_actualiza_saldo():
    """CP-06: Retirar un monto positivo menor al saldo disminuye el saldo correctamente."""
    atm = ATM()
    atm.retirar(RETIRO_VALIDO)
    esperado = 1000.0 - RETIRO_VALIDO
    caso("CP-06", f"Retiro de S/.{RETIRO_VALIDO} → saldo = S/.{esperado:.2f}", atm.consultar_saldo(), esperado)

def test_retiro_exactamente_el_saldo():
    """CP-07: Retirar exactamente el saldo disponible deja el saldo en cero. (límite exacto)"""
    atm = ATM()
    exito, _ = atm.retirar(1000)
    caso("CP-07", "Retiro exacto del saldo → saldo = S/.0.00", atm.consultar_saldo(), 0.0)

def test_retiro_mayor_al_saldo_rechazado():
    """CP-08: Intentar retirar más del saldo disponible debe ser rechazado. (límite superior)"""
    atm = ATM()
    exito, _ = atm.retirar(1500)
    caso("CP-08", "Retiro S/.1500 > saldo S/.1000 es rechazado (éxito=False)", exito, False)

def test_retiro_cero_rechazado():
    """CP-09: Retirar cero debe ser rechazado. (límite inferior)"""
    atm = ATM()
    exito, _ = atm.retirar(0)
    caso("CP-09", "Retiro de S/.0 es rechazado (éxito=False)", exito, False)

def test_retiro_negativo_rechazado():
    """CP-10: Retirar un monto negativo debe ser rechazado."""
    atm = ATM()
    exito, _ = atm.retirar(RETIRO_NEGATIVO)
    caso("CP-10", f"Retiro de S/.{RETIRO_NEGATIVO} es rechazado (éxito=False)", exito, False)

def test_saldo_sin_cambio_tras_retiro_excedente():
    """CP-11: El saldo no debe cambiar si el retiro supera el saldo disponible."""
    atm = ATM()
    atm.retirar(2000)
    caso("CP-11", "Saldo inalterado tras retiro excedente (S/.2000)", atm.consultar_saldo(), 1000.0)

def test_saldo_sin_cambio_tras_retiro_invalido():
    """CP-12: El saldo no debe cambiar si el retiro es de monto cero."""
    atm = ATM()
    atm.retirar(0)
    caso("CP-12", "Saldo inalterado tras retiro inválido (0)", atm.consultar_saldo(), 1000.0)


# ─────────────────────────────────────────────
#  GRUPO 4 — Operaciones encadenadas
# ─────────────────────────────────────────────

def test_operaciones_multiples_en_secuencia():
    """CP-13: Varias operaciones consecutivas deben reflejar el saldo acumulado correcto."""
    atm = ATM()           # saldo = 1000
    atm.depositar(SEQ_DEP_1)
    atm.retirar(SEQ_RET_1)
    atm.depositar(SEQ_DEP_2)
    atm.retirar(SEQ_RET_2)
    esperado = 1000.0 + SEQ_DEP_1 - SEQ_RET_1 + SEQ_DEP_2 - SEQ_RET_2
    caso("CP-13", f"Operaciones encadenadas: saldo final = S/.{esperado:.2f}", atm.consultar_saldo(), esperado)

def test_retiro_invalido_no_afecta_operaciones_siguientes():
    """CP-14: Un retiro inválido no debe afectar las operaciones posteriores."""
    atm = ATM()           # saldo = 1000
    atm.retirar(5000)     # rechazado, saldo = 1000
    atm.depositar(POST_INVALIDO_DEPOSITO)
    esperado = 1000.0 + POST_INVALIDO_DEPOSITO
    caso("CP-14", f"Retiro inválido no bloquea operaciones futuras → saldo = S/.{esperado:.2f}", atm.consultar_saldo(), esperado)


# ─────────────────────────────────────────────
#  EJECUCIÓN PRINCIPAL
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   CASOS DE PRUEBA — Mini Simulador ATM")
    print("=" * 60)

    print("\n  [ GRUPO 1 ] Consulta de saldo")
    test_saldo_inicial()

    print("\n  [ GRUPO 2 ] Depósito de dinero")
    test_deposito_positivo_actualiza_saldo()
    test_deposito_cero_rechazado()
    test_deposito_negativo_rechazado()
    test_saldo_sin_cambio_tras_deposito_invalido()

    print("\n  [ GRUPO 3 ] Retiro de dinero")
    test_retiro_valido_actualiza_saldo()
    test_retiro_exactamente_el_saldo()
    test_retiro_mayor_al_saldo_rechazado()
    test_retiro_cero_rechazado()
    test_retiro_negativo_rechazado()
    test_saldo_sin_cambio_tras_retiro_excedente()
    test_saldo_sin_cambio_tras_retiro_invalido()

    print("\n  [ GRUPO 4 ] Operaciones encadenadas")
    test_operaciones_multiples_en_secuencia()
    test_retiro_invalido_no_afecta_operaciones_siguientes()

    # ── Resumen ──
    pasaron = sum(1 for _, _, e in resultados if "PASÓ" in e)
    fallaron = sum(1 for _, _, e in resultados if "FALLÓ" in e)
    total = len(resultados)

    print("\n" + "=" * 60)
    print(f"   RESUMEN FINAL: {pasaron}/{total} casos pasaron  |  {fallaron} fallaron")
    print("=" * 60 + "\n")
