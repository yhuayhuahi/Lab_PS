import pytest
from reembolsos import calcular_reembolso

def test_valores_limite_antelacion():
    # Estos son mis casos cuando tenemos > 72 horas
    assert calcular_reembolso(100, 73, False) == 100.0
    assert calcular_reembolso(100, 80, False) == 100.0

    # Cuando tenemos exactamente 72 horas nos correspondria 50% 
    assert calcular_reembolso(100, 72, False) == 100.0

    # Cuando tenemos exactamente 24 horas nos correspondria 50% 
    assert calcular_reembolso(100, 24, False) == 100.0

    # Estos son mis casos cuando tenemos < 24 horas
    assert calcular_reembolso(100, 23, False) == 0.0
    assert calcular_reembolso(100, 20, False) == 0.0

def test_regla_vip_prioridad():
    # Cuando nuestro VIP tuviera < 24 horas debe recibir 50%
    assert calcular_reembolso(100, 2, True) == 50.0
    # Cuando nuestro VIP tuviera > 72 horas debe recibir 100%, màs que los 50% que le corresponderia por ser VIP
    assert calcular_reembolso(100, 80, True) == 100.0

def test_proteccion_errores():
    # En caso tuvieramos un monto de reserva negativo debemos lanzar un ValueError
    with pytest.raises(ValueError):
        calcular_reembolso(-50, 48, False)