from evaluar import evaluar_rendimiento
import random

def test_evaluar_rendimiento_insuficiente():
    assert evaluar_rendimiento(random.randint(0,10)) == "Insuficiente"

def test_evaluar_rendimiento_regular():
    assert evaluar_rendimiento(random.randint(11, 15)) == "Regular"

def test_evaluar_rendimiento_excelente():
    assert evaluar_rendimiento(random.randint(16, 20)) == "Excelente"

def test_evaluar_rendimiento_fuera_rango_menor():
    assert evaluar_rendimiento(-2) == "Nota fuera de rango"

def test_evaluar_rendimiento_fuera_rango_mayor():
    assert evaluar_rendimiento(23) == "Nota fuera de rango"
